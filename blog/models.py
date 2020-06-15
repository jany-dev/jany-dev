from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel


from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock

body = StreamField([
    ('heading', blocks.CharBlock(classname="full title", icon="title")),
    ('paragraph', blocks.RichTextBlock(icon="pilcrow")),
    ('embed', EmbedBlock(icon="media")),
])

class HomePageCarouselImages(Orderable):
    """ Between 1 and 5 images for the home page carousel. """
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
    'wagtailimages.Image',
    null=True,
    blank=True,
    on_delete=models.SET_NULL
)
content_panels = Page.content_panels + [
    InlinePanel("carousel_images")
]
panels = [
    ImageChooserPanel("carousel_image")

]

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


def get_context(self, request):
        # Update context to include only published posts,
        # in reverse chronological order
        context = super(BlogIndexPage, self).get_context(request)
        live_blogpages = self.get_children().live()
        context['blogpages'] = live_blogpages.order_by('-first_published_at')
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]

    # in the imports


# in your BlogPage class
image = models.ForeignKey(
    'wagtailimages.Image',
    null=True,
    blank=True,
    on_delete=models.SET_NULL
)

# in your content_panels for BlogPage
ImageChooserPanel('image'),

