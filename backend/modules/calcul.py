def inference(prompt, tokenizer,model):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generated_ids = model.generate(
        input_ids,
        max_length=input_ids.shape[1] + 256,
        temperature=0.7,
        # top_p=0.80,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(generated_ids[0])