from vocal import plugin
import wikipedia

class SearchPlugin(plugin.PluginObject):

    def get_response(intent, slots):
        default = "Je n'ai malheureusement pas bien compris"
        return getattr(SearchPlugin(), 'case_' + intent, lambda: default)(slots)

    def has_intent(intent):
        intent_list=["askdefinition"]
        return any(elem == intent for elem in intent_list)

    def case_askdefinition(self, slots):
        wikipedia.set_lang("fr")
        search = wikipedia.search(slots[0]["rawValue"])
        if(len(search) > 0):
            return wikipedia.summary(search[0], sentences=2)
        else:
            return "je n'ai malheureusement rien trouvé à ce sujet"
