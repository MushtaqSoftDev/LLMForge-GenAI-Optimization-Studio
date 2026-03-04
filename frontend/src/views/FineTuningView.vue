<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import api from "../services/api";
import { getFriendlyAuthError } from "../utils/errors";

const { t } = useI18n();

const openSections = ref(new Set(["intro", "comparison", "demo", "code"]));
const running = ref(false);
const result = ref(null);
const error = ref(null);

function toggleSection(key) {
  openSections.value.has(key)
    ? openSections.value.delete(key)
    : openSections.value.add(key);
  openSections.value = new Set(openSections.value);
}

async function runDemo() {
  running.value = true;
  error.value = null;
  result.value = null;
  try {
    const { data } = await api.post("/api/finetune/demo");
    result.value = data;
  } catch (err) {
    error.value = getFriendlyAuthError(
      err,
      "The fine-tuning demo is not available here (it needs several minutes and more memory). Use the code example below and run it locally with Python and PyTorch to try full fine-tuning and LoRA/PEFT."
    );
  } finally {
    running.value = false;
  }
}

const codeEdited = ref(`# CPU-compatible: full fine-tuning (no peft)
# For LoRA/Prefix Tuning, install: pip install peft  (requires full PyTorch + GPU)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import Dataset
from rouge_score import rouge_scorer

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

train_data = [
    {"input": "Summarize: The cat sat on the mat.", "output": "A cat sat on a mat."},
    {"input": "Summarize: The weather is sunny and 25 degrees.", "output": "Sunny, 25 degrees."},
    {"input": "Summarize: Python is simple and readable.", "output": "Python is simple."},
]

def tokenize(ex):
    i = tokenizer(ex["input"], truncation=True, padding="max_length", max_length=128)
    i["labels"] = tokenizer(ex["output"], truncation=True, padding="max_length", max_length=64)["input_ids"]
    return i
ds = Dataset.from_list(train_data).map(tokenize)

# Full fine-tune (works on CPU)
trainer = Seq2SeqTrainer(
    model=model, tokenizer=tokenizer, train_dataset=ds,
    args=Seq2SeqTrainingArguments(
        output_dir="./ft_out", num_train_epochs=5, per_device_train_batch_size=2,
        learning_rate=5e-5, logging_steps=2, save_strategy="no")
)
trainer.train()

# Compare base vs fine-tuned + ROUGE
test = "Summarize: Machine learning is a subset of AI that lets computers learn from data."
ref = "Machine learning is an AI subset for learning from data."
def gen(m,t): return tokenizer.decode(m.generate(**tokenizer(t,return_tensors="pt"), max_new_tokens=50)[0], skip_special_tokens=True)

base = AutoModelForSeq2SeqLM.from_pretrained(model_name)
scorer = rouge_scorer.RougeScorer(["rouge1","rouge2","rougeL"], use_stemmer=True)
ft_out = gen(trainer.model, test)
print("Base:", gen(base, test))
print("Fine-tuned:", ft_out)
print("ROUGE-1:", scorer.score(ref, ft_out)["rouge1"].fmeasure)`);

const copySuccess = ref(false);
function copyCode() {
  navigator.clipboard.writeText(codeEdited.value);
  copySuccess.value = true;
  setTimeout(() => (copySuccess.value = false), 1500);
}
</script>

<template>
  <div class="ft-page">
    <h1 class="page-title">{{ t("fineTuning.pageTitle") }}</h1>

    <!-- Intro -->
    <section class="ft-section card">
      <button class="section-toggle" @click="toggleSection('intro')">
        <span>{{ t("fineTuning.introTitle") }}</span>
        <span class="chev">{{ openSections.has('intro') ? '&#9650;' : '&#9660;' }}</span>
      </button>
      <div v-if="openSections.has('intro')" class="section-content">
        <p>{{ t("fineTuning.introDesc") }}</p>

        <!-- Full fine-tuning -->
        <div class="method-card">
          <h3>{{ t("fineTuning.fullTitle") }}</h3>
          <p>{{ t("fineTuning.fullDesc") }}</p>
          <div class="pros-cons">
            <span class="pros">{{ t("fineTuning.fullPros") }}</span>
            <span class="cons">{{ t("fineTuning.fullCons") }}</span>
          </div>
        </div>

        <!-- LoRA -->
        <div class="method-card">
          <h3>{{ t("fineTuning.peftTitle") }}</h3>
          <p>{{ t("fineTuning.peftDesc") }}</p>
          <div class="pros-cons">
            <span class="pros">{{ t("fineTuning.peftPros") }}</span>
            <span class="cons">{{ t("fineTuning.peftCons") }}</span>
          </div>
        </div>

        <!-- Soft Prompting -->
        <div class="method-card">
          <h3>{{ t("fineTuning.softTitle") }}</h3>
          <p>{{ t("fineTuning.softDesc") }}</p>
          <div class="pros-cons">
            <span class="pros">{{ t("fineTuning.softPros") }}</span>
            <span class="cons">{{ t("fineTuning.softCons") }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Comparison table -->
    <section class="ft-section card">
      <button class="section-toggle" @click="toggleSection('comparison')">
        <span>{{ t("fineTuning.comparisonTitle") }}</span>
        <span class="chev">{{ openSections.has('comparison') ? '&#9650;' : '&#9660;' }}</span>
      </button>
      <div v-if="openSections.has('comparison')" class="section-content">
        <table class="comp-table">
          <thead>
            <tr>
              <th>{{ t("fineTuning.compMethod") }}</th>
              <th>{{ t("fineTuning.compParams") }}</th>
              <th>{{ t("fineTuning.compGPU") }}</th>
              <th>{{ t("fineTuning.compQuality") }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ t("fineTuning.compFull") }}</td>
              <td>{{ t("fineTuning.compFullParams") }}</td>
              <td>{{ t("fineTuning.compFullGPU") }}</td>
              <td>{{ t("fineTuning.compFullQuality") }}</td>
            </tr>
            <tr>
              <td>{{ t("fineTuning.compLoRA") }}</td>
              <td>{{ t("fineTuning.compLoRAParams") }}</td>
              <td>{{ t("fineTuning.compLoRAGPU") }}</td>
              <td>{{ t("fineTuning.compLoRAQuality") }}</td>
            </tr>
            <tr>
              <td>{{ t("fineTuning.compSoft") }}</td>
              <td>{{ t("fineTuning.compSoftParams") }}</td>
              <td>{{ t("fineTuning.compSoftGPU") }}</td>
              <td>{{ t("fineTuning.compSoftQuality") }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Live Demo -->
    <section class="ft-section card">
      <button class="section-toggle" @click="toggleSection('demo')">
        <span>{{ t("fineTuning.demoTitle") }}</span>
        <span class="chev">{{ openSections.has('demo') ? '&#9650;' : '&#9660;' }}</span>
      </button>
      <div v-if="openSections.has('demo')" class="section-content">
        <p>{{ t("fineTuning.demoDesc") }}</p>
        <p class="demo-hint">{{ t("fineTuning.demoHostedNote") }}</p>

        <button
          class="btn btn-primary"
          :disabled="running"
          @click="runDemo"
        >
          {{ running ? t("fineTuning.demoRunning") : t("fineTuning.demoRunBtn") }}
        </button>

        <div v-if="error" class="demo-error">{{ error }}</div>

        <div v-if="result?.gpu_message" class="demo-gpu-warning">
          {{ result.gpu_message }}
        </div>

        <div v-if="result" class="demo-results">
          <div class="demo-row">
            <strong>{{ t("fineTuning.demoTestInput") }}:</strong>
            <pre>{{ result.test_input }}</pre>
          </div>
          <div class="demo-row">
            <strong>{{ t("fineTuning.demoReference") }}:</strong>
            <pre>{{ result.reference }}</pre>
          </div>
          <div class="demo-row base">
            <strong>{{ t("fineTuning.demoBaseLabel") }}:</strong>
            <pre>{{ result.base_output }}</pre>
          </div>
          <div class="demo-row finetuned">
            <strong>{{ t("fineTuning.demoFineTunedLabel") }} ({{ result.method_used === 'lora' ? 'LoRA' : 'Full' }}):</strong>
            <pre>{{ result.finetuned_output }}</pre>
          </div>
          <div class="demo-row rouge">
            <strong>{{ t("fineTuning.demoRougeLabel") }} ({{ result.method_used === 'lora' ? 'LoRA' : 'Full' }}):</strong>
            <div class="rouge-scores">
              <span>ROUGE-1: <b>{{ result.rouge.rouge1 }}</b></span>
              <span>ROUGE-2: <b>{{ result.rouge.rouge2 }}</b></span>
              <span>ROUGE-L: <b>{{ result.rouge.rougeL }}</b></span>
            </div>
          </div>
          <div v-if="result.finetuned_prefix_output" class="demo-row finetuned prefix">
            <strong>{{ t("fineTuning.demoFineTunedPrefixLabel") }}:</strong>
            <pre>{{ result.finetuned_prefix_output }}</pre>
          </div>
          <div v-if="result.rouge_prefix" class="demo-row rouge">
            <strong>{{ t("fineTuning.demoRougePrefixLabel") }}:</strong>
            <div class="rouge-scores">
              <span>ROUGE-1: <b>{{ result.rouge_prefix.rouge1 }}</b></span>
              <span>ROUGE-2: <b>{{ result.rouge_prefix.rouge2 }}</b></span>
              <span>ROUGE-L: <b>{{ result.rouge_prefix.rougeL }}</b></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Code Example -->
    <section class="ft-section card">
      <button class="section-toggle" @click="toggleSection('code')">
        <span>{{ t("fineTuning.codeTitle") }}</span>
        <span class="chev">{{ openSections.has('code') ? '&#9650;' : '&#9660;' }}</span>
      </button>
      <div v-if="openSections.has('code')" class="section-content">
        <p>{{ t("fineTuning.codeDesc") }}</p>
        <div class="code-actions">
          <button class="btn btn-primary btn-sm" @click="copyCode">
            {{ copySuccess ? "Copied!" : "Copy code" }}
          </button>
        </div>
        <textarea v-model="codeEdited" class="code-block" spellcheck="false"></textarea>
      </div>
    </section>
  </div>
</template>

<style scoped>
.ft-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px 20px;
}
.page-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 24px;
}
.ft-section {
  margin-bottom: 16px;
}
.section-toggle {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: var(--bg-tertiary);
  border: none;
  color: var(--accent);
  font-size: 1rem;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
  border-radius: var(--radius-lg);
}
.section-toggle:hover { background: var(--border); }
.chev { font-size: 0.7rem; color: var(--text-muted); }
.section-content {
  padding: 16px 18px;
}
.section-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 14px;
}
.method-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  margin-bottom: 12px;
}
.method-card h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.pros-cons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 8px;
  font-size: 0.8rem;
}
.pros {
  color: var(--success);
  background: rgba(76, 175, 80, 0.1);
  padding: 4px 10px;
  border-radius: 4px;
}
.cons {
  color: var(--danger);
  background: rgba(239, 83, 80, 0.1);
  padding: 4px 10px;
  border-radius: 4px;
}

/* comparison table */
.comp-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}
.comp-table th,
.comp-table td {
  padding: 10px 12px;
  border: 1px solid var(--border);
  text-align: left;
}
.comp-table th {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-weight: 600;
}
.comp-table td {
  color: var(--text-secondary);
}

/* demo */
.demo-results {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.demo-row {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px;
}
.demo-row strong {
  display: block;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.demo-row pre {
  font-size: 0.85rem;
  color: var(--text-primary);
  white-space: pre-wrap;
  margin: 0;
}
.demo-row.base {
  border-left: 3px solid var(--warning);
}
.demo-row.finetuned {
  border-left: 3px solid var(--success);
}
.demo-row.rouge {
  border-left: 3px solid var(--accent);
}
.rouge-scores {
  display: flex;
  gap: 16px;
  font-size: 0.88rem;
  color: var(--text-primary);
}
.rouge-scores b {
  color: var(--accent);
}
.demo-hint {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 12px;
}
.demo-error {
  margin-top: 12px;
  color: var(--danger);
  font-size: 0.85rem;
}
.demo-gpu-warning {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 152, 0, 0.15);
  border: 1px solid var(--warning);
  border-radius: var(--radius);
  color: var(--text-primary);
  font-size: 0.9rem;
}

/* code block */
.code-actions {
  margin-bottom: 8px;
}
.code-block {
  display: block;
  width: 100%;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  font-family: ui-monospace, "Cascadia Code", "Fira Code", monospace;
  font-size: 0.78rem;
  line-height: 1.5;
  color: var(--text-primary);
  resize: vertical;
  min-height: 320px;
  max-height: 600px;
}
</style>
