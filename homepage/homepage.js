var areas = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
        url: 'reference-areas.json',
        cache: false,
    },
});

$('#bloodhound .typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'areas',
        display: 'name',
        source: areas
    });

$('.typeahead').bind('typeahead:select', function (ev, suggestion) {
    location.href = suggestion.path;
});
