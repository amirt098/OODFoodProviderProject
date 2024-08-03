import logging
from django.db import IntegrityError
from utils.date_time import interfaces as date_time_interfaces
from apps.accounts.interfaces import UserClaim
from . import interfaces
from .models import EventOrCommand

logger = logging.getLogger(__name__)


class EventBus(interfaces.AbstractEventBus):
    def __init__(
            self,
            claim: UserClaim,
            date_time_utils: date_time_interfaces.AbstractDateTimeUtils,
    ):
        self.claim = claim
        self.date_time_utils = date_time_utils
        self.subscribers = []

    def emit(self, caller: UserClaim, event_or_command: interfaces.EventOrCommand):
        logger.info(f'\n\ncaller: {caller}, event_or_command: {event_or_command}')
        try:
            EventOrCommand.objects.create(
                uid=event_or_command.uid,
                emitter_uid=caller.user_uid,
                event_type=event_or_command.event_type,
                payload_json=event_or_command.payload.model_dump_json(),
                created_at=self.date_time_utils.get_current_timestamp(),
            )
            for subscriber in self.subscribers:
                logger.debug(f"subscriber: {subscriber}")
                self._push_if_matched(subscriber, caller, event_or_command)
        except IntegrityError as e:
            logger.warning(f'Integrity error: {e}')
        except Exception as e:
            logger.warning(f'\n\nan exception occurred during emission: {e}')

    def subscribe(self, caller: UserClaim, match_string: str, listener: interfaces.AbstractEventListener):
        logger.info(f'caller: {caller}, match_string: {match_string}, listener: {listener}')
        self.subscribers.append({
            'match_string': match_string,
            'listener': listener,
        })

    def _push_if_matched(self, subscriber, emitter_claim: UserClaim, event_or_command: interfaces.EventOrCommand):
        is_matched = self._is_matched(subscriber['match_string'], emitter_claim.user_uid, event_or_command.event_type)
        logger.info(f'matched: {is_matched}')
        if is_matched:
            try:
                subscriber['listener'].on_event_or_command(emitter_claim, event_or_command)
            except Exception as e:
                logger.warning(f'an exception occurred during push: {e}')

    def _is_matched(self, match_string: str, emitter_uid: str, event_type: str) -> bool:
        sp = match_string.split('/')
        if sp[0] != '*' and sp[0] != emitter_uid:
            return False
        if sp[1] != '*' and sp[1] != event_type:
            return False
        return True
