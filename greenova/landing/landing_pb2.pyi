from typing import Type, List
from google.protobuf.message import Message

class NewsletterSignupRequest(Message):
    email: str

class NewsletterSignupResponse(Message):
    success: bool
    message: str

class Feature(Message):
    title: str
    description: str

class Stat(Message):
    name: str
    value: int

class Testimonial(Message):
    name: str
    content: str

class LandingPageContent(Message):
    hero_title: str
    hero_subtitle: str
    features: List[Feature]
    stats: List[Stat]
    benefits: List[str]
    testimonials: List[Testimonial]
    cta_title: str
    cta_subtitle: str
