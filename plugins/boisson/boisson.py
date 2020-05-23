class BoissonPlugin:

    def get_response(intent, slots):
        response_list = {
            "askBeverage": "je te prépare ta"+slots[0]["rawValue"],
        }
        return response_list.get(intent, "je n'ai pas bien compris votre demande")

    def has_intent(intent):
        intent_list=["askBeverage"]
        return any(elem == intent for elem in intent_list)
