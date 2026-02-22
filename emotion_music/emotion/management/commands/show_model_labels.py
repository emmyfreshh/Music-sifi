from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Print id2label for a Hugging Face wav2vec2 audio-classification model."

    def add_arguments(self, parser):
        parser.add_argument("model_id", type=str)

    def handle(self, *args, **opts):
        model_id = opts["model_id"]
        from transformers import AutoModelForAudioClassification

        m = AutoModelForAudioClassification.from_pretrained(model_id)
        id2label = getattr(m.config, "id2label", {})
        labels = sorted({str(v).lower() for v in id2label.values()})
        self.stdout.write(f"Model: {model_id}")
        self.stdout.write("Labels:")
        for l in labels:
            self.stdout.write(f"- {l}")