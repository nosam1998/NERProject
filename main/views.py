import spacy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from spacy import displacy
from django.views.decorators.csrf import csrf_exempt


nlp = spacy.load('en_core_web_trf')


class Home(View):
    def get(self, request):
        return render(request, 'predictorform.html')


@method_decorator(csrf_exempt, name='dispatch')
class Results(View):
    def get(self, request):
        pass

    def post(self, request):
        data = request.POST.get("data")
        doc = nlp(data)
        prediction = []
        ent_to_keep = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT",
                       "EVENT", "WORK_OF_ART", "LANGUAGE", "MONEY", "LAW"]
        for ent in doc.ents:
            entity = (ent.text, ent.label_)
            if ent.label_ in ent_to_keep:
                prediction.append(entity)
        if len(prediction) == 0:
            prediction = "There were no recognizable entities"

        html = displacy.render(doc, style="ent")
        html = html.replace("\n\n", "\n")
        html_wrapper = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

        return JsonResponse({"data": data, "prediction": prediction})
