from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Fellowship(models.Model):
    """
    Represents fellowship groups. Scoped per organization (church).
    """
    
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="fellowships",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Fellowship'
        verbose_name_plural = 'Fellowships'
        unique_together = [('organization', 'name')]
    
    def __str__(self):
        return self.name


class Person(models.Model):
    """
    Represents an individual connected to the church.

    Title indicates their role/position. We keep basic contact details so
    that follow-up is possible later.
    """

    PROPHET = "prophet"
    GENERAL_OVERSEER = "general_overseer"
    SENIOR_ARCHBISHOP_EMERITUS = "senior_archbishop_emeritus"
    SENIOR_ARCHBISHOP = "senior_archbishop"
    SENIOR_DEPUTY_ARCHBISHOP = "senior_deputy_archbishop"
    DEPUTY_ARCHBISHOP = "deputy_archbishop"
    BISHOP = "bishop"
    OVERSEER = "overseer"
    SENIOR_PASTOR = "senior_pastor"
    PASTOR = "pastor"
    SISTER = "sister"
    BROTHER = "brother"
    VISITOR = "visitor"
    EMPLOYEE = "employee"

    TITLE_CHOICES = [
        (PROPHET, "Prophet"),
        (GENERAL_OVERSEER, "General Overseer"),
        (SENIOR_ARCHBISHOP_EMERITUS, "Senior Archbishop Emeritus"),
        (SENIOR_ARCHBISHOP, "Senior Archbishop"),
        (SENIOR_DEPUTY_ARCHBISHOP, "Senior Deputy Archbishop"),
        (DEPUTY_ARCHBISHOP, "Deputy Archbishop"),
        (BISHOP, "Bishop"),
        (OVERSEER, "Overseer"),
        (SENIOR_PASTOR, "Senior Pastor"),
        (PASTOR, "Pastor"),
        (SISTER, "Sister"),
        (BROTHER, "Brother"),
        (VISITOR, "Visitor"),
        (EMPLOYEE, "Employee"),
    ]

    MALE = "male"
    FEMALE = "female"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]

    MEMBER = "member"
    VISITOR_TYPE = "visitor"
    MEMBER_VISITOR_CHOICES = [
        (MEMBER, "Member"),
        (VISITOR_TYPE, "Visitor"),
    ]

    # Age range choices for filtering
    AGE_0_12 = "0-12"
    AGE_13_17 = "13-17"
    AGE_18_25 = "18-25"
    AGE_26_35 = "26-35"
    AGE_36_50 = "36-50"
    AGE_51_65 = "51-65"
    AGE_OVER_65 = "65+"
    
    AGE_CHOICES = [
        (AGE_0_12, "Children (0-12)"),
        (AGE_13_17, "Teens (13-17)"),
        (AGE_18_25, "Young Adults (18-25)"),
        (AGE_26_35, "Adults (26-35)"),
        (AGE_36_50, "Adults (36-50)"),
        (AGE_51_65, "Adults (51-65)"),
        (AGE_OVER_65, "Seniors (65+)"),
    ]

    # Fellowship groups (legacy choices for backward compatibility)
    MENS_FELLOWSHIP = "mens_fellowship"
    WOMENS_FELLOWSHIP = "womens_fellowship"
    YOUTH_FELLOWSHIP = "youth_fellowship"
    CHILDREN = "children"
    CHOIR = "choir"
    USHERING = "ushering"
    PRAYER = "prayer"
    NONE = "none"
    OTHER_FELLOWSHIP = "other"
    
    # Legacy choices for backward compatibility
    FELLOWSHIP_CHOICES = [
        (MENS_FELLOWSHIP, "Men's Fellowship"),
        (WOMENS_FELLOWSHIP, "Women's Fellowship"),
        (YOUTH_FELLOWSHIP, "Youth Fellowship"),
        (CHILDREN, "Children"),
        (CHOIR, "Choir"),
        (USHERING, "Ushering"),
        (PRAYER, "Prayer"),
        (NONE, "None"),
        (OTHER_FELLOWSHIP, "Other"),
    ]

    # Department choices for service areas
    MUSIC = "music"
    USHERING = "ushering"
    PRAYER = "prayer"
    MEDIA = "media"
    CHILDREN_MINISTRY = "children_ministry"
    YOUTH_MINISTRY = "youth_ministry"
    OUTREACH = "outreach"
    ADMINISTRATION = "administration"
    MAINTENANCE = "maintenance"
    SECURITY = "security"
    HOSPITALITY = "hospitality"
    TEACHING = "teaching"
    NONE_DEPT = "none"
    OTHER_DEPT = "other"
    
    DEPARTMENT_CHOICES = [
        (MUSIC, "Music"),
        (USHERING, "Ushering"),
        (PRAYER, "Prayer"),
        (MEDIA, "Media"),
        (CHILDREN_MINISTRY, "Children Ministry"),
        (YOUTH_MINISTRY, "Youth Ministry"),
        (OUTREACH, "Outreach"),
        (ADMINISTRATION, "Administration"),
        (MAINTENANCE, "Maintenance"),
        (SECURITY, "Security"),
        (HOSPITALITY, "Hospitality"),
        (TEACHING, "Teaching"),
        (NONE_DEPT, "None"),
        (OTHER_DEPT, "Other"),
    ]

    full_name = models.CharField(max_length=200)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    title = models.CharField(
        max_length=35,
        choices=TITLE_CHOICES,
        default=BROTHER,
    )
    first_visit_date = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    fellowship = models.ForeignKey(
        Fellowship, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='people'
    )
    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        default=NONE_DEPT,
        blank=True
    )
    residence = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="people",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name

    def age(self):
        """Return age in years, or None if no date_of_birth."""
        if self.date_of_birth:
            return (date.today() - self.date_of_birth).days // 365
        return None

    def get_fellowship_display(self):
        """Return fellowship display name, handling both FK and legacy choices."""
        if self.fellowship:
            return str(self.fellowship)
        return "—"


class Service(models.Model):
    """
    A single service/meeting (e.g. Sunday service, worship practice, etc.).
    """

    EVANGELISM = "evangelism"
    CRUSADE = "crusade"
    PRAYERS = "prayers"
    HOME_FELLOWSHIP = "home_fellowship"
    WORSHIP_PRACTICE = "worship_practice"
    WORSHIP_EXTRAVAGANZA = "worship_extravaganza"
    SATURDAY_PREPARATIONS = "saturday_preparations"
    SUNDAY_SERVICE = "sunday_service"
    OTHERS = "others"

    SERVICE_TYPE_CHOICES = [
        (EVANGELISM, "Evangelism"),
        (CRUSADE, "Crusade"),
        (PRAYERS, "Prayers"),
        (HOME_FELLOWSHIP, "Home Fellowship"),
        (WORSHIP_PRACTICE, "Worship Practice"),
        (WORSHIP_EXTRAVAGANZA, "Worship Extravaganza"),
        (SATURDAY_PREPARATIONS, "Saturday Preparations"),
        (SUNDAY_SERVICE, "Sunday Service"),
        (OTHERS, "Others"),
    ]

    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPE_CHOICES,
        default=SUNDAY_SERVICE,
    )
    title = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="services",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="services_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-start_time"]
        unique_together = ("date", "service_type", "title")

    def __str__(self) -> str:
        label = self.title or dict(self.SERVICE_TYPE_CHOICES).get(self.service_type, "Service")
        return f"{label} on {self.date}"


class Attendance(models.Model):
    """
    A record that a given person attended a specific service.

    It also captures whether they are a member, visitor, or marked as
    'healed_of_the_LORD' for that service, and optional notes.
    """

    MEMBER = "member"
    VISITOR = "visitor"
    HEALED = "healed_of_the_LORD"
    CATEGORY_CHOICES = [
        (MEMBER, "Member"),
        (VISITOR, "Visitor"),
        (HEALED, "Healed of the LORD"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="attendances")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="attendances")

    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    present = models.BooleanField(default=True)
    is_first_time_visitor = models.BooleanField(default=False)
    is_healed_this_service = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("service", "person")
        ordering = ["service", "person"]

    def __str__(self) -> str:
        return f"{self.person} at {self.service}"
