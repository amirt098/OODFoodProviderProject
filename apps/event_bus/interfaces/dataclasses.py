from pydantic import BaseModel
import lib.data_classes as lib_data_classes


class EventOrCommand(BaseModel):
    uid: str  # for duplicate emit prevention
    event_type: lib_data_classes.CustomStringValidator.max_length_string(128)  # usually upper case
    payload: BaseModel  # each event has its own payload. the emitter should document this.
    # timeout: int = 0 # in milliseconds. 0 means try once. None means try infinitely till all listeners get the event
    # run_at: int = None  # if None, it will be emitted ASAP
