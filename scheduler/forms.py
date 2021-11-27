from django import forms

choices = [
    (1, "Strongly Dislike"),
    (2, "Somewhat Dislike"),
    (3, "Neutral"),
    (4, "Somewhat Like"),
    (5, "Strongly Like")
]


class PreferenceForm(forms.Form):
    music = forms.IntegerField(label="Music:", required=True, widget=forms.Select(choices=choices))
    visual = forms.IntegerField(label="Visual:", required=True, widget=forms.Select(choices=choices))
    performing = forms.IntegerField(label="Performing:", required=True, widget=forms.Select(choices=choices))
    film = forms.IntegerField(label="Film:", required=True, widget=forms.Select(choices=choices))
    lectures = forms.IntegerField(label="Lectures", required=True, widget=forms.Select(choices=choices))
    fashion = forms.IntegerField(label="Fashion", required=True, widget=forms.Select(choices=choices))
    food = forms.IntegerField(label="Food", required=True, widget=forms.Select(choices=choices))
    festivals = forms.IntegerField(label="Festivals", required=True, widget=forms.Select(choices=choices))
    charity = forms.IntegerField(label="Charity", required=True, widget=forms.Select(choices=choices))
    sports = forms.IntegerField(label="Sports", required=True, widget=forms.Select(choices=choices))
    nightlife = forms.IntegerField(label="Night Life", required=True, widget=forms.Select(choices=choices))
    family = forms.IntegerField(label="Family", required=True, widget=forms.Select(choices=choices))


class EventSearchForm(forms.Form):
    start_time = forms.DateTimeField(label="Free From:", required=True, widget=forms.DateTimeInput(attrs={
        "type": "datetime-local"
    }))
    end_time = forms.DateTimeField(label="Free Until:", required=True, widget=forms.DateTimeInput(attrs={
        "type": "datetime-local"
    }))
    address1 = forms.CharField(label="Street Address:", max_length=200, required=True)
    city = forms.CharField(label="City:", max_length=200, required=True)
    state = forms.CharField(label="State:", max_length=200, required=True)
    country = forms.CharField(label="Country:", max_length=200, required=True)
    commute_hrs = forms.IntegerField(
        label="How many hours will you spend travelling:",
        required=True,
    )
    commute_mins = forms.IntegerField(
        label="How many minutes will you spend travelling:",
        required=True,
        widget=forms.Select(choices=[(i * 5, i * 5) for i in range(12)]),
    )
    cost = forms.FloatField(label="Enter your maximum budget:", required=True, min_value=0.0)
    optimized = forms.BooleanField(label="Optimize Schedule (You might need to wait a few minutes)", required=False)
