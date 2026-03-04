import asyncio

from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.config import settings
from app.models import User

router = APIRouter()

GPU_UNAVAILABLE_MSG = (
    "GPU is not available. LoRA and Prefix Tuning require a GPU for efficient fine-tuning. "
    "Full fine-tuning was used instead (runs on CPU)."
)


def _run_full_finetune(model_name, tokenizer, train_data, tokenize_fn):
    """Full fine-tuning — works on CPU."""
    from transformers import (
        AutoModelForSeq2SeqLM,
        Seq2SeqTrainer,
        Seq2SeqTrainingArguments,
    )
    from datasets import Dataset
    import tempfile

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    dataset = Dataset.from_list(train_data).map(tokenize_fn)
    tmp_dir = tempfile.mkdtemp()

    trainer = Seq2SeqTrainer(
        model=model,
        args=Seq2SeqTrainingArguments(
            output_dir=tmp_dir,
            num_train_epochs=5,
            per_device_train_batch_size=2,
            learning_rate=5e-5,
            logging_steps=2,
            save_strategy="no",
            report_to="none",
        ),
        train_dataset=dataset,
        tokenizer=tokenizer,
    )
    trainer.train()
    return trainer.model


def _run_lora_finetune(model_name, tokenizer, train_data, tokenize_fn):
    """LoRA fine-tuning — requires GPU for efficiency."""
    from transformers import (
        AutoModelForSeq2SeqLM,
        Seq2SeqTrainer,
        Seq2SeqTrainingArguments,
    )
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import Dataset
    import tempfile

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    lora_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q", "v"],
    )
    peft_model = get_peft_model(model, lora_config)
    dataset = Dataset.from_list(train_data).map(tokenize_fn)
    tmp_dir = tempfile.mkdtemp()

    trainer = Seq2SeqTrainer(
        model=peft_model,
        args=Seq2SeqTrainingArguments(
            output_dir=tmp_dir,
            num_train_epochs=5,
            per_device_train_batch_size=2,
            learning_rate=3e-4,
            logging_steps=2,
            save_strategy="no",
            report_to="none",
        ),
        train_dataset=dataset,
        tokenizer=tokenizer,
    )
    trainer.train()
    return trainer.model


def _run_demo():
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    from datasets import Dataset
    from rouge_score import rouge_scorer

    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    base_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    train_data = [
        {"input": "Summarize: The cat sat on the mat and looked out the window.", "output": "A cat sat on a mat watching."},
        {"input": "Summarize: The weather today is sunny with temperatures around 25 degrees.", "output": "Today is sunny and 25 degrees."},
        {"input": "Summarize: Python is a programming language known for its simplicity.", "output": "Python is a simple programming language."},
        {"input": "Summarize: The students worked hard and achieved great exam results.", "output": "Students worked hard and got great results."},
    ]

    def tokenize(example):
        inputs = tokenizer(example["input"], truncation=True, padding="max_length", max_length=128)
        targets = tokenizer(example["output"], truncation=True, padding="max_length", max_length=64)
        inputs["labels"] = targets["input_ids"]
        return inputs

    test_input = "Summarize: Machine learning is a subset of AI that lets computers learn from data."
    reference = "Machine learning is an AI subset for learning from data."

    def generate(m, text):
        inputs = tokenizer(text, return_tensors="pt")
        out = m.generate(**inputs, max_new_tokens=50)
        return tokenizer.decode(out[0], skip_special_tokens=True)

    gpu_available = torch.cuda.is_available()

    gpu_message = None
    if gpu_available:
        try:
            ft_model = _run_lora_finetune(model_name, tokenizer, train_data, tokenize)
            method_used = "lora"
        except Exception:
            ft_model = _run_full_finetune(model_name, tokenizer, train_data, tokenize)
            method_used = "full"
            gpu_message = "LoRA failed (e.g. CPU-only PyTorch). Full fine-tuning used instead."
    else:
        ft_model = _run_full_finetune(model_name, tokenizer, train_data, tokenize)
        method_used = "full"
        gpu_message = GPU_UNAVAILABLE_MSG

    base_output = generate(base_model, test_input)
    ft_output = generate(ft_model, test_input)

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, ft_output)

    result = {
        "test_input": test_input,
        "reference": reference,
        "base_output": base_output,
        "finetuned_output": ft_output,
        "finetuned_prefix_output": None,
        "rouge": {
            "rouge1": round(scores["rouge1"].fmeasure, 4),
            "rouge2": round(scores["rouge2"].fmeasure, 4),
            "rougeL": round(scores["rougeL"].fmeasure, 4),
        },
        "rouge_prefix": None,
        "method_used": method_used,
        "gpu_available": gpu_available,
        "gpu_message": gpu_message,
    }
    return result


@router.post("/demo")
async def run_finetune_demo(user: User = Depends(get_current_user)):
    if settings.DISABLE_FINETUNE_DEMO.strip().lower() in ("true", "1", "yes"):
        raise HTTPException(
            status_code=503,
            detail="The fine-tuning demo is disabled on this server (it needs several minutes and more memory than hosted environments allow). Run the code example locally with Python and PyTorch to try full fine-tuning and LoRA/PEFT.",
        )
    result = await asyncio.to_thread(_run_demo)
    return result
