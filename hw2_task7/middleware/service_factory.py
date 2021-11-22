"""

Students: Ignore this file ... ...


"""


from application_services.address_services.smarty_address_service import SmartyAddressService


class ServiceFactory():

    @staticmethod
    def get_address_service():
        return SmartyAddressService()