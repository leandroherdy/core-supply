class PhoneFormatter:
    """
    Formats telephone numbers in the E.164 standard.
    """

    @staticmethod
    def format_phone_number(phone):
        """
        Formats a telephone number to the E.164 standard.
        Removes special characters and adds the country code +55 for Brazilian numbers.

        :param phone: String containing the phone number.
        :return: String formatted in the E.164 standard.
        """
        if not phone:
            return None
        phone = phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        return f'+55{phone}'
