
import json
import logging
import os
from django.shortcuts import get_object_or_404
from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.branding.models import SavedBrand, LogoDesign

from .serializers import BrandNameRequestSerializer, SavedBrandSerializer, LogoPromptSerializer

logger = logging.getLogger(__name__)


class BrandNameGeneratorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BrandNameRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return Response(
                {"error": "AI service is not configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        data = serializer.validated_data

        prompt = f"""
Generate 10 unique, creative brand name ideas for a startup.

Business idea: {data['business_idea']}
Industry: {data['industry']}
Brand style: {data['style']}

Return only valid JSON in this format:
{{
  "brand_names": [
    {{
      "name": "ExampleName",
      "meaning": "Short explanation",
      "tagline": "Short memorable tagline"
    }}
  ]
}}

Requirements:
- Generate exactly 10 names.
- Keep names easy to pronounce and remember.
- Avoid explanations outside the JSON.
- Do not claim that domain names or trademarks are available.
"""

        try:
            client = OpenAI(api_key=api_key)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional startup naming expert. Return valid JSON only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
            )

            result_text = completion.choices[0].message.content
            result = json.loads(result_text)

            names = result.get("brand_names")

            if not isinstance(names, list) or len(names) != 10:
                return Response(
                    {"error": "AI returned an unexpected response. Please retry."},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            return Response(
                {
                    "business_idea": data["business_idea"],
                    "industry": data["industry"],
                    "style": data["style"],
                    "brand_names": names,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception("Brand name generation failed")
            return Response(
                {"error": "Brand name generation failed. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )



class SavedBrandListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands = SavedBrand.objects.filter(user=request.user)
        serializer = SavedBrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SavedBrandSerializer(data=request.data)

        if serializer.is_valid():
            brand = serializer.save(
                user=request.user
            )
            return Response(
                SavedBrandSerializer(brand).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SavedBrandDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        brand = get_object_or_404(
            SavedBrand,
            pk=pk,
            user=request.user,
        )
        brand.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

from .models import LogoDesign
from .serializers import LogoDesignSerializer


class LogoConceptGeneratorView(APIView):
    """Turn a natural-language brief into several editable logo design recipes."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoPromptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        styles = [choice[0] for choice in LogoDesign.STYLE_CHOICES]
        symbols = [choice[0] for choice in LogoDesign.SYMBOL_CHOICES]
        palettes = [choice[0] for choice in LogoDesign.PALETTE_CHOICES]
        prompt_lower = data["prompt"].casefold()

        # Offline fallback: useful for common English, Hindi and Hinglish cues.
        def has(*terms):
            return any(term.casefold() in prompt_lower for term in terms)

        symbol = "monogram"
        for terms, candidate in [
            (("lion", "sher", "शेर", "सिंह"), "lion"),
            (("shield", "सुरक्षा", "रक्षा", "ढाल"), "shield"),
            (("wave", "समुद्र", "लहर", "ocean"), "wave"),
            (("flame", "fire", "आग", "ज्वाला"), "flame"),
            (("hexagon", "षट्भुज"), "hexagon"),
            (("globe", "world", "दुनिया", "पृथ्वी"), "globe"),
            (("cube", "3d cube", "घन"), "cube"),
            (("crown", "ताज", "मुकुट"), "crown"),
            (("bolt", "lightning", "बिजली"), "bolt"),
            (("flower", "फूल", "floral"), "flower"),
            (("leaf", "eco", "nature", "हरा-भरा", "पत्ता"), "leaf"),
            (("mountain", "पहाड़", "पर्वत"), "mountain"),
            (("orbit", "space", "अंतरिक्ष", "planet"), "orbit"),
            (("spark", "star", "तारा", "innovation"), "spark"),
            (("flower", "bloom", "फूल"), "bloom"),
        ]:
            if has(*terms):
                symbol = candidate
                break

        palette = "violet"
        for terms, candidate in [
            (("black and gold", "black-gold", "gold", "सुनहरा", "सोना", "golden"), "gold"),
            (("green", "हरा", "हरी", "eco", "nature"), "forest"),
            (("blue", "नीला", "नीली", "ocean", "समुद्र"), "ocean"),
            (("red", "लाल", "ember", "fire", "आग"), "ember"),
            (("pink", "गुलाबी", "rose"), "rose"),
            (("sunset", "sunrise", "सूर्यास्त", "sunset colors"), "sunset"),
            (("neon", "cyberpunk", "neon", "नियॉन"), "midnight"),
            (("earth tone", "earthy", "brown", "मिट्टी", "भूरा"), "earth"),
            (("yellow", "orange", "पीला", "नारंगी", "citrus"), "citrus"),
            (("black and white", "monochrome", "काला-सफेद", "सादा काला"), "mono"),
            (("purple", "violet", "बैंगनी", "जामुनी"), "violet"),
        ]:
            if has(*terms):
                palette = candidate
                break

        style = "modern"
        for terms, candidate in [
            (("minimal", "minimalist", "सादा", "मिनिमल"), "minimal"),
            (("luxury", "premium", "royal", "शाही", "लग्जरी", "elegant"), "premium"),
            (("professional", "corporate", "विश्वसनीय"), "professional"),
            (("geometric", "geometry", "ज्यामितीय"), "geometric"),
            (("futuristic", "sci-fi", "techy", "भविष्य", "फ्यूचरिस्टिक"), "futuristic"),
            (("playful", "cute", "fun", "मजेदार", "प्यारा"), "playful"),
            (("organic", "natural", "प्राकृतिक"), "organic"),
            (("vintage", "retro", "पुराना अंदाज़"), "vintage"),
            (("creative", "artistic", "कलात्मक"), "creative"),
        ]:
            if has(*terms):
                style = candidate
                break

        fallback_concepts = [
            {"style": style, "symbol": symbol, "palette": palette, "tagline": data.get("tagline", ""), "reason": "Closest local match to your brief"},
            {"style": "minimal", "symbol": symbol, "palette": "mono", "tagline": data.get("tagline", ""), "reason": "A clean, high-contrast alternative"},
            {"style": "geometric", "symbol": "hexagon", "palette": "ocean", "tagline": data.get("tagline", ""), "reason": "A structured, modern alternative"},
            {"style": "creative", "symbol": "spark", "palette": "sunset", "tagline": data.get("tagline", ""), "reason": "A more expressive color direction"},
        ]

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return Response({"concepts": fallback_concepts, "mode": "local_fallback", "notice": "AI interpretation is not configured; showing built-in style matches."}, status=status.HTTP_200_OK)

        try:
            allowed = {
                "styles": [label for value, label in LogoDesign.STYLE_CHOICES],
                "style_values": styles,
                "symbols": symbols,
                "palettes": palettes,
            }
            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "You are a multilingual logo art director. Understand the user's brief in any language. "
                        "Return JSON only with a concepts array of exactly four objects. Each object must have "
                        "style, symbol, palette, tagline, reason. Choose style, symbol and palette values only "
                        "from these allowed values: " + json.dumps(allowed) + ". "
                        "Do not translate or rewrite the brand name. The result is a recipe for an editable vector logo, not a raster image."
                    )},
                    {"role": "user", "content": json.dumps({"brief": data["prompt"], "brand_name": data.get("name", ""), "industry": data.get("industry", ""), "tagline": data.get("tagline", "")}, ensure_ascii=False)},
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
            )
            result = json.loads(completion.choices[0].message.content or "{}")
            concepts = result.get("concepts")

            if not isinstance(concepts, list) or len(concepts) != 4:
                raise ValueError("AI must return exactly four logo concepts")

            # Normalize AI values and recover from small formatting differences.
            normalized_concepts = []

            for index, concept in enumerate(concepts):
                if not isinstance(concept, dict):
                    raise ValueError(f"AI concept {index + 1} is not an object")

                def normalize_choice(value, allowed_values, default):
                    if not isinstance(value, str):
                        return default

                    cleaned = value.strip().lower()

                    for allowed_value in allowed_values:
                        if cleaned == allowed_value.strip().lower():
                            return allowed_value

                    return default

                fallback = fallback_concepts[index]

                normalized_concepts.append({
                    "style": normalize_choice(
                        concept.get("style"), styles, fallback["style"]
                    ),
                    "symbol": normalize_choice(
                        concept.get("symbol"), symbols, fallback["symbol"]
                    ),
                    "palette": normalize_choice(
                        concept.get("palette"), palettes, fallback["palette"]
                    ),
                    "tagline": (
                        concept.get("tagline")
                        if isinstance(concept.get("tagline"), str)
                        else fallback["tagline"]
                    ),
                    "reason": (
                        concept.get("reason")
                        if isinstance(concept.get("reason"), str)
                        else fallback["reason"]
                    ),
                })

            return Response(
                {"concepts": normalized_concepts, "mode": "ai"},
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Logo prompt interpretation failed; using local fallback")
            return Response({"concepts": fallback_concepts, "mode": "local_fallback", "notice": "AI could not interpret this prompt right now; showing built-in style matches instead."}, status=status.HTTP_200_OK)


class LogoDesignListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        designs = LogoDesign.objects.filter(user=request.user)
        return Response(LogoDesignSerializer(designs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LogoDesignSerializer(data=request.data)
        if serializer.is_valid():
            design = serializer.save(user=request.user)
            return Response(LogoDesignSerializer(design).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoDesignDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(LogoDesign, pk=pk, user=request.user)

    def get(self, request, pk):
        design = self.get_object(request, pk)
        return Response(LogoDesignSerializer(design).data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        design = self.get_object(request, pk)
        serializer = LogoDesignSerializer(design, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        design = self.get_object(request, pk)
        design.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
