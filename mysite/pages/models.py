from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from home.models import BoutonBlock, GalerieItemBlock, LayoutMixin


class IllustrationsPage(LayoutMixin, Page):
    image_couverture = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    mots_cles = models.CharField(
        max_length=200, blank=True,
        help_text="Séparés par des virgules. Ex : animaux, forêt, bébé",
    )
    body = StreamField(
        [
            ("titre", blocks.CharBlock(form_classname="title", label="Titre de section")),
            ("texte", blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])),
            ("image", ImageChooserBlock(label="Illustration")),
            ("galerie_boutons", blocks.ListBlock(GalerieItemBlock(), label="Galerie d'illustrations")),
            ("bouton", BoutonBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("image_couverture"),
        FieldPanel("mots_cles"),
        FieldPanel("body"),
    ]

    @property
    def liste_mots_cles(self):
        return [m.strip() for m in self.mots_cles.split(",") if m.strip()]

class AProposPage(LayoutMixin, Page):
    max_count = 1  # une seule page « À propos » sur le site

    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        help_text="Image affichée à gauche.",
    )
    paragraphe = RichTextField(
        blank=True, features=["bold", "italic", "link", "ol", "ul"],
    )

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("paragraphe"),
    ]

class ContactPage(LayoutMixin, Page):
    max_count = 1  # une seule page Contact sur le site

    body = StreamField(
        [
            ("sous_titre", blocks.CharBlock(form_classname="title", label="Sous-titre")),
            ("paragraphe", blocks.RichTextBlock(
                features=["bold", "italic", "link"],
                label="Paragraphe",
            )),
            ("bouton", BoutonBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
class FormulaireChamp(AbstractFormField):
    page = ParentalKey(
        "FormulairePage", on_delete=models.CASCADE, related_name="form_fields"
    )


class FormulairePage(LayoutMixin, AbstractEmailForm):
    max_count = 1  # un seul formulaire de contact sur le site

    intro = RichTextField(
        blank=True, features=["bold", "italic", "link"],
        help_text="Texte affiché au-dessus du formulaire.",
    )
    texte_merci = RichTextField(
        blank=True, features=["bold", "italic", "link"],
        help_text="Message affiché après l'envoi.",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champ du formulaire"),
        FieldPanel("texte_merci"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("from_address"), FieldPanel("to_address")]
                ),
                FieldPanel("subject"),
            ],
            heading="Envoi par e-mail",
        ),
    ]
class MentionsLegalesPage(LayoutMixin, Page):
    max_count = 1  # une seule page de mentions légales

    contenu = RichTextField(
        features=["h2", "h3", "bold", "italic", "link", "ol", "ul"],
        blank=True,
        help_text="Utilise les titres (H2/H3) pour séparer les rubriques.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("contenu"),
    ]
class GaleriePage(LayoutMixin, Page):
    galerie = StreamField(
        [
            ("image", GalerieItemBlock(label="Image")),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("galerie"),
    ]