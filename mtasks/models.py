import enum
import logging
from django.core.mail import *
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from forgor_adm.utils.mail import send_mail_async as send_mail
from hashlib import sha1


logger = logging.getLogger(__name__)

number_tr = _("number")

TASK_PRIORITY_FIELDS = ('state', '-priority', '-deadline')


class State(enum.Enum):
    TO_DO = '00-to-do'
    IN_PROGRESS = '10-in-progress'
    BLOCKED = '20-blocked'
    DONE = '30-done'
    DISMISSED = '40-dismissed'


class Priority(enum.Enum):
    
    LOW = '00-low'
    #lol
    NORMAL = '10-normal'
    HIGH = '20-high'
    CRITICAL = '30-critical'


class TaskManager(models.Manager):

    def others(self, pk, **kwargs):
        return self.exclude(pk=pk).filter(**kwargs)


class Task(models.Model):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        indexes = [
            models.Index(fields=TASK_PRIORITY_FIELDS, name='mtasks_task_priority_idx'),
        ]

    STATES = (
        (State.TO_DO.value, _('To Do')),
        (State.IN_PROGRESS.value, _('In Progress')),
        (State.BLOCKED.value, _('Blocked')),
        (State.DONE.value, _('Done')),
        (State.DISMISSED.value, _('Dismissed'))
    )

    PRIORITIES = (
        (Priority.LOW.value, _('Low')),
        (Priority.NORMAL.value, _('Normal')),
        (Priority.HIGH.value, _('High')),
        (Priority.CRITICAL.value, _('Critical')),
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATES, default=State.TO_DO.value)
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default=Priority.NORMAL.value)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    objects = TaskManager()

    def __str__(self):
        return "[%s] %s" % (self.number, self.title)

    @property
    def number(self) -> str:
        return "{:08d}".format(self.pk)

    

    

    def send_new_task_email(self):
        emails_to = []
        if settings.TASKS_SEND_EMAILS_TO_ASSIGNED and self.user and self.user.email:
            emails_to.append(self.user.email)
        if len(emails_to):
            logger.info("[Task #%s] Sending task creation email to: %s", self.number, emails_to)
            vals = {
                "id": self.number,
                "user": str(self.user) if self.user else '(Not assigned yet)',
                "title": self.title,
                "description": self.description or '-',
                "sign": settings.SITE_HEADER,
            }
            if settings.TASKS_VIEWER_ENABLED:
                email_template = settings.MTASKS_EMAIL_WITH_URL
                vals["url"] = self.get_tasks_viewer_url()
            else:
                email_template = settings.MTASKS_EMAIL_WITHOUT_URL
            try:
                send_mail(
                    '[{app}] [#{id}] New Task Created'.format(app=settings.APP_NAME, id=self.number),
                    email_template.format(**vals),
                    settings.APP_EMAIL,
                    emails_to,
                )
            except Exception as e:
                logger.warning("[Task #%s] Error trying to send the task creation email - %s: %s",
                               self.number, e.__class__.__name__, str(e))

    def get_tasks_viewer_url(self):
        salt = settings.TASKS_VIEWER_HASH_SALT
        if not settings.DEBUG and salt == '1two3':
            logger.warning("Insecure salt code used to send email orders, do NOT use it in PRODUCTION")
        token = "{}-{}".format(salt, self.pk)
        token = sha1(token.encode('utf-8')).hexdigest()
        return settings.TASKS_VIEWER_ENDPOINT.format(number=self.number, token=token)


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Check List")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(_("description"), max_length=200)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return self.item_description
