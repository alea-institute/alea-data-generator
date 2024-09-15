"""
Faker sampling interface designed to simplify and improve on default faker behavior.
"""

# imports
from typing import Callable, Dict, Optional

# packages
from faker import Faker

# project

ZERO_ARG_METHODS = [
    # true zero arg methods
    "ascii_company_email",
    "ascii_email",
    "ascii_free_email",
    "ascii_safe_email",
    "company_email",
    "domain_name",
    "domain_word",
    "email",
    "free_email",
    "free_email_domain",
    "hostname",
    "safe_domain_name",
    "safe_email",
    "slug",
    "user_name",
    # one arg methods with defaults
    "aba",
    "address",
    "administrative_unit",
    "am_pm",
    "android_platform_token",
    "bank_country",
    "basic_phone_number",
    "bban",
    "bs",
    "building_number",
    "catch_phrase",
    "century",
    "city",
    "city_prefix",
    "city_suffix",
    "color_name",
    "company",
    "company_suffix",
    "country",
    "country_calling_code",
    "cryptocurrency",
    "cryptocurrency_code",
    "cryptocurrency_name",
    "currency",
    "currency_code",
    "currency_name",
    "current_country",
    "current_country_code",
    "day_of_month",
    "day_of_week",
    "ein",
    "emoji",
    "firefox",
    "first_name",
    "first_name_female",
    "first_name_male",
    "first_name_nonbinary",
    "get_providers",
    "hex_color",
    "http_method",
    "iana_id",
    "iban",
    "internet_explorer",
    "invalid_ssn",
    "ios_platform_token",
    "ipv4_network_class",
    "itin",
    "job",
    "language_code",
    "language_name",
    "last_name",
    "last_name_female",
    "last_name_male",
    "last_name_nonbinary",
    "latitude",
    "latlng",
    "license_plate",
    "linux_platform_token",
    "linux_processor",
    "locale",
    "localized_ean13",
    "localized_ean8",
    "longitude",
    "mac_platform_token",
    "mac_processor",
    "military_apo",
    "military_dpo",
    "military_ship",
    "military_state",
    "month",
    "month_name",
    "msisdn",
    "name",
    "name_female",
    "name_male",
    "name_nonbinary",
    "null_boolean",
    "opera",
    "passport_dob",
    "passport_full",
    "passport_number",
    "phone_number",
    "postalcode",
    "postalcode_plus4",
    "postcode",
    "prefix",
    "prefix_female",
    "prefix_male",
    "prefix_nonbinary",
    "pricetag",
    "pytimezone",
    "random_digit",
    "random_digit_above_two",
    "random_digit_not_null",
    "random_digit_not_null_or_empty",
    "random_digit_or_empty",
    "random_letter",
    "random_lowercase_letter",
    "random_uppercase_letter",
    "rgb_color",
    "rgb_css_color",
    "ripe_id",
    "safari",
    "safe_color_name",
    "safe_hex_color",
    "secondary_address",
    "state",
    "street_address",
    "street_name",
    "street_suffix",
    "suffix",
    "suffix_female",
    "suffix_male",
    "suffix_nonbinary",
    "timezone",
    "tld",
    "uri_extension",
    "uri_page",
    "user_agent",
    "vin",
    "windows_platform_token",
    "year",
    "zipcode",
    "zipcode_plus4",
    # two arg methods with defaults
    "binary",
    "boolean",
    "country_code",
    "credit_card_full",
    "credit_card_number",
    "credit_card_provider",
    "credit_card_security_code",
    "currency_symbol",
    "date_object",
    "ean8",
    "file_extension",
    "http_status_code",
    "ipv6",
    "isbn10",
    "isbn13",
    "localized_ean",
    "location_on_land",
    "mac_address",
    "md5",
    "mime_type",
    "nic_handle",
    "numerify",
    "passport_dates",
    "passport_gender",
    "passport_owner",
    "postalcode_in_state",
    "postcode_in_state",
    "pybool",
    "pyobject",
    "random_element",
    "random_letters",
    "sbn9",
    "seed_instance",
    "sha1",
    "sha256",
    "simple_profile",
    "ssn",
    "swift8",
    "time_delta",
    "time_object",
    "unix_device",
    "unix_partition",
    "uri_path",
    "url",
    "uuid4",
    "zipcode_in_state",
    # three arg methods with defaults
    "color_hsl",
    "color_hsv",
    "color_rgb",
    "color_rgb_float",
    "coordinate",
    "date",
    "date_this_century",
    "date_this_decade",
    "date_this_month",
    "date_this_year",
    "date_time",
    "date_time_ad",
    "ean",
    "ean13",
    "file_name",
    "future_date",
    "future_datetime",
    "ipv4_private",
    "ipv4_public",
    "local_latlng",
    "nic_handles",
    "paragraphs",
    "past_date",
    "past_datetime",
    "profile",
    "sentences",
    "state_abbr",
    "swift11",
    "text",
    "time",
    "unix_time",
    "uri",
    "word",
]


def get_faker_instance(
    locale: Optional[str] = None, seed: Optional[int] = None
) -> Faker:
    """
    Get a faker instance with the specified locale.

    Args:
        locale (Optional[str]): The locale to use for the faker instance.

    Returns:
        Faker: The faker instance.
    """
    # create the faker instance
    instance = Faker(locale)

    # set the seed if provided
    if seed is not None:
        Faker.seed(seed)

    # return the instance
    return instance


def get_faker_tag_map(faker_instance: Faker) -> Dict[str, Callable]:
    """
    Get a map of faker methods by name.

    Args:
        faker_instance (Faker): The faker instance to use.

    Returns:
        Dict[str, Callable]: The map of faker methods by name.
    """
    # zero-arg methods
    method_map: Dict[str, Callable] = {}
    for method_name in ZERO_ARG_METHODS:
        method_map[method_name] = getattr(faker_instance, method_name)

    # return the method map
    return method_map


# create the shared faker instance
FAKER_INSTANCE = get_faker_instance()

# create the default tag map
FAKER_TAG_MAP = get_faker_tag_map(FAKER_INSTANCE)
