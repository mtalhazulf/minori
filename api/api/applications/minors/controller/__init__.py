from .controller_attendance import (
    minors_attendance_arg_get,
    minors_attendance_month_arg_get,
    minors_attendance_post,
)
from .controller_minor import (
    minors_minor_all_get,
    minors_minor_arg_get,
    minors_minor_arg_post,
    minors_minor_arg_put,
    minors_minor_disable_arg_put,
    minors_minor_generate_summary_post,
    minors_minor_get,
    minors_minor_post,
    minors_minor_present_get,
    minors_minor_present_prices_get,
)
from .controller_price import (
    minors_minor_id_calculate_get,
    minors_minor_id_price_get,
    minors_minor_id_price_post,
    minors_minor_id_price_timestamp_delete,
    minors_minor_id_price_timestamp_patch,
    minors_minor_price_get,
)
