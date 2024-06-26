from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from common.models import AbstractModel
from main import settings


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        print(f"Creating user with email: {email}")  # Debugging line
        user.save(using=self._db)
        return user

    def create_user(self, email, password, confirm_password, **kwargs):
        if not email:
            raise ValueError(_("Email is required."))
        if not password:
            raise ValueError(_("Password is required."))
        if password != confirm_password:
            raise ValueError(_("Passwords do not match."))

        kwargs["is_admin"] = False
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs["is_admin"] = True
        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, AbstractModel):
    email = models.EmailField(
        _("Email"),
        max_length=128,
        unique=True,
        db_index=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=32,
        blank=True,
    )

    verification_token = models.CharField(
        _("Verification Token"),
        max_length=100,
        blank=True,
    )

    is_active = models.BooleanField(
        _("Active"),
        help_text=_("Designates whether this user can access their account."),
        default=False,
    )

    is_admin = models.BooleanField(
        _("Admin"),
        help_text=_("Designates whether the user can log into this admin site."),
        default=False,
    )

    bio = models.TextField(blank=True)
    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email} ({self.name})"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    def get_all_permissions(self, obj=None):
        return []

    #######################################
    def get_short_name(self):
        # Example implementation, you can adjust as per your user model
        return self.name

    def generate_verification_token(self):
        self.verification_token = default_token_generator.make_token(self)
        self.save()
        print(
            f"Generated token for {self.email}: {self.verification_token}"
        )  # Debugging line

    # Override save method to ensure token generation on save
    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.generate_verification_token()
        super().save(*args, **kwargs)

    def send_verification_email(self):
        import logging

        logger = logging.getLogger("myapp.emails")

        from django.core.mail import send_mail
        from django.core.mail import BadHeaderError

        self.generate_verification_token()  # Generate and save token before sending email

        verification_url = f"http://localhost:8000/register/verify-email/?token={self.verification_token}"
        recipient_email = self.email
        try:
            print(
                f"Sending verification email to {recipient_email} with token {self.verification_token}"
            )  # Debugging line
            send_mail(
                subject="Verify your email",
                message=f"Click the link to verify your email: {verification_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
            )
            logger.info(f"Verification email sent to {self.email}")

        except BadHeaderError:
            print("Invalid header found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"Failed to send verification email to {self.email}: {e}")

    #######################################

    class Meta(AbstractModel.Meta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
