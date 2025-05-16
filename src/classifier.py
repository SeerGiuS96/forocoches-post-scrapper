from .models import ContentCategory

class ContentClassifier:
    @staticmethod
    def classify(text: str) -> ContentCategory:
        text = text.lower()
        
        housing_keywords = ["piso", "alquiler", "hipoteca"]
        relationship_keywords = ["novia", "pareja", "relación"]
        marriage_keywords = ["casarse", "boda", "matrimonio"]
        
        if any(kw in text for kw in housing_keywords):
            return ContentCategory.HOUSING
        elif any(kw in text for kw in relationship_keywords):
            return ContentCategory.RELATIONSHIP
        elif any(kw in text for kw in marriage_keywords):
            return ContentCategory.MARRIAGE
        return ContentCategory.GENERAL