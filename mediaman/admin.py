from django.contrib import admin
from django.core import urlresolvers

mediafile_readonly = ('file_size', 'uploaded_by', 'mime_type',
        'original_filename', 'original_path', 'original_filedate',)


class MOInline(admin.TabularInline):
#    model = MuseumObject.related_documents.through
    fields = ('museumobject', 'item_link',)
    readonly_fields = ('item_link',)

    def item_link(self, obj):
        if obj.museumobject:
            mo = obj.museumobject
            admin_url = urlresolvers.reverse('admin:cat_museumobject_change', args=(mo.id,))
            return '<a href="%s">%s</a>' % (admin_url, mo.__unicode__())
        else:
            return ''
    item_link.allow_tags = True
    verbose_name_plural = 'Related museum items'

    raw_id_fields = ('museumobject',)


class PersonInline(admin.TabularInline):
#    model = Person.related_documents.through
    fields = ('person', 'person_link',)
    readonly_fields = ('person_link',)

    def person_link(self, obj):
        if obj.person:
            p = obj.person
            admin_url = urlresolvers.reverse('admin:parties_person_change', args=(p.id,))
            return '<a href="%s">%s</a>' % (admin_url, p.display_name)
        else:
            return ''
    person_link.allow_tags = True
    verbose_name_plural = 'Related people'
    raw_id_fields = ('person',)


def make_public(modeladmin, request, queryset):
    queryset.update(public=True)


def make_private(modeladmin, request, queryset):
    queryset.update(public=False)


class MediaFileAdmin(admin.ModelAdmin):
    ordering = ('-upload_date',)
    actions = [make_public, make_private]

    def has_add_permission(self, request):
        '''Always deny adding in admin

        Files should always be uploaded through the bulk upload tool
        '''
        return False


class DocumentAdmin(MediaFileAdmin):
    readonly_fields = mediafile_readonly + ('view_document',)
    fields = mediafile_readonly + ('document_text', 'public', 'view_document',)

    def view_document(self, obj):
        doc = obj.document
        return '<a href="%s">%s</a>' % (doc.url, doc.name)
    view_document.allow_tags = True
    inlines = [MOInline, PersonInline]

    def related_items(self, obj):
        return ", ".join([str(m.registration_number) for m in obj.museumobject_set.all()])

    def people(self, obj):
        return ", ".join([str(p) for p in obj.related_people.all()])
    list_display = ('__unicode__', 'related_items', 'people', 'upload_date', 'public')

#admin.site.register(Document, DocumentAdmin)


class ArtefactRepresentationAdmin(MediaFileAdmin):
    readonly_fields = ('item_link',) + mediafile_readonly + ('thumbnail',)
    fields = ('public',) + readonly_fields
    list_display = ('__unicode__', 'artefact', 'upload_date', 'public')

    def item_link(self, obj):
        if obj.artefact:
            admin_url = urlresolvers.reverse('admin:cat_museumobject_change', args=(obj.artefact_id,))
            return '<a href="%s">%s</a>' % (admin_url, obj.artefact)
        else:
            return ''
    item_link.allow_tags = True

    def thumbnail(self, obj):
        try:
            thumb_opts = {'size': (64, 64), 'watermark': ''}
            thumb = obj.image.get_thumbnail(thumb_opts)
            return '<a href="%s"><img src="%s"></a>' % (obj.image.url, thumb.url)
        except:
            return 'Error generating thumbnail'
    thumbnail.allow_tags = True


#admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)
