from bert import bert


paragraph = "This section describes how to install the integrated directional Antenna . \n" \
            "The integrated directional Antenna is not applicable to rail installation , ceiling installation , " \
            "or horizontal installation .\nTo install the Antenna , do the following :\n" \
            "step 1: Hook the Antenna onto the Radio Core.\n" \
            "step 2: Route the RF cables through the cable holders and attach the cables to the cable clips.\n" \
            "step 3: Connect the RF cables to the RF connectors.\n" \
            "step 4: Close the Antenna.\n" \
            "step 5: Secure the Antenna by tightening the screw."


model = bert.load_bert()
print(paragraph + "\n")
while True:

    query = input("What is your query?\n")
    answer = bert.bert_answer(model, query, paragraph)
    print("Bert\'s answer: ", answer)
