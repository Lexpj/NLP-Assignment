from transformers import BartForConditionalGeneration, BartTokenizer

class BART:
    
    def __init__(self):
        self.model = BartForConditionalGeneration.from_pretrained("facebook/bart-large", forced_bos_token_id=0)
        self.tok = BartTokenizer.from_pretrained("facebook/bart-large")

    def gen(self,sentence, rhymeword):
        """
        BART model generate function
        :param sentence: full sentence as prompt
        :param rhymeword: rhymeword to be used in the generated sentence
        :return: generated sentence
        """
        example_english_phrase = sentence + " <mask> " + rhymeword
        batch = self.tok(example_english_phrase, return_tensors="pt")
        generated_ids = self.model.generate(batch["input_ids"])
        res = self.tok.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(res)
        return(res)
