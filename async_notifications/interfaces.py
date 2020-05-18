
class NewsLetterInterface:
    name = ""
    field_map = {}
    form = None
    model = None

    def get_form(self, data=None):
        if data is None:
            form = self.form()
        else:
            form = self.form(data)
        return form

    def set_form(self, form):
        self.form = form

    def get_exclude(self):
        exclude = {}
        excludeemail = self.form.cleaned_data['excludeemail']
        if excludeemail:
            exclude[self.field_map['exclude']['excludeemail']] = excludeemail.replace(" ", '').split(',')
            if not exclude[self.field_map['exclude']['excludeemail']][0]:
                exclude[self.field_map['exclude']['excludeemail']].pop(0)
            self.excludedata = set(exclude[self.field_map['exclude']['excludeemail']])
        return exclude

    def get_filters(self):
        filters = {}
        self.form.is_valid()
        filterfields = self.field_map['filter'].keys()
        for field in filterfields:
            if field in self.form.cleaned_data and self.form.cleaned_data[field]:
                filters[self.field_map['filter'][field]] = self.form.cleaned_data[field]
        return filters

    def get_queryset(self):
        filters = self.get_filters()
        excludes = self.get_exclude()
        self.queryset = self.model.objects.all()
        if filters:
            self.queryset = self.queryset.filter(**filters)
        if excludes:
            self.queryset = self.queryset.exclude(**excludes)

        return self.queryset

    def get_emails(self):
        return []

    def get_emails_instance(self):
        return (None, None)