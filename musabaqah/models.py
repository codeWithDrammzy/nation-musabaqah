from django.db import models
from django.contrib.auth.hashers import make_password, check_password


NIGERIAN_STATES = (
    ('AB', 'Abia'),
    ('AD', 'Adamawa'),
    ('AK', 'Akwa Ibom'),
    ('AN', 'Anambra'),
    ('BA', 'Bauchi'),
    ('BY', 'Bayelsa'),
    ('BE', 'Benue'),
    ('BO', 'Borno'),
    ('CR', 'Cross River'),
    ('DE', 'Delta'),
    ('EB', 'Ebonyi'),
    ('ED', 'Edo'),
    ('EK', 'Ekiti'),
    ('EN', 'Enugu'),
    ('FC', 'FCT'),
    ('GO', 'Gombe'),
    ('IM', 'Imo'),
    ('JI', 'Jigawa'),
    ('KD', 'Kaduna'),
    ('KN', 'Kano'),
    ('KT', 'Katsina'),
    ('KE', 'Kebbi'),
    ('KO', 'Kogi'),
    ('KW', 'Kwara'),
    ('LA', 'Lagos'),
    ('NA', 'Nasarawa'),
    ('NI', 'Niger'),
    ('OG', 'Ogun'),
    ('ON', 'Ondo'),
    ('OS', 'Osun'),
    ('OY', 'Oyo'),
    ('PL', 'Plateau'),
    ('RI', 'Rivers'),
    ('SO', 'Sokoto'),
    ('TA', 'Taraba'),
    ('YB', 'Yobe'),
    ('ZA', 'Zamfara'),
)

CATEGORY =(
    ('1st', '60Hibz'),
    ('2nd', '40Hibz'),
    ('3rd', '20Hibz'),
    ('4th', '10Hibz'),
    ('5th', '2Hibz')

)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class StateUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    role = models.CharField(max_length=20, default='cordinator')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    state = models.CharField(max_length=2, choices=NIGERIAN_STATES)
    password = models.CharField(max_length=128, default=make_password('1234'))  # default hashed password

    def __str__(self):
        return self.first_name + " " + self.last_name

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Participant(models.Model):
    state_user = models.ForeignKey('StateUser', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=11, unique=True)
    hibz = models.CharField(choices=CATEGORY, max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hibz', 'gender'], name='unique_hibz_per_gender')
        ]


def __str__(self):
    return self.first_name + " "+ self.last_name

@property
def state(self):
    return self.state_user.state