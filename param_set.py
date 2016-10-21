import lib.params as pm

print("Would you like this bot to be annoying?")
annoy_answer = input("[]: ")
annoy_answer.strip(' ')
annoy_answer = annoy_answer.lower()

if annoy_answer == "true" or annoy_answer == "yes":
    annoy = True
elif annoy_answer == "false" or annoy_answer == "no":
    annoy = False
else:
    raise ValueError("Please enter 'True', 'False', 'yes', or 'no'")

pm.edit_shelf({'ANNOY': annoy})
