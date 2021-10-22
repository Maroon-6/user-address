import database_services.RDBService as d_service


class AddressResource():

    def __init__(self):
        pass

    def get_address_by_template(template):
        res=d_service.find_by_template('hw1_user', 'addresses',
                                       template, None)
        return res

    def post_address_by_template(template):
        res = d_service.insert_by_template('hw1_user', 'addresses',
                                         template,None)
        return res

    def put_address_by_id(template,id):
        res = d_service.update_by_id('hw1_user', 'addresses',
                                         template,id)
        return res

    def delete_address_by_id(id):
        res = d_service.delete_by_id('hw1_user', 'addresses',
                                           id)
        return res

    def get_address_by_userid(template):
        res=d_service.get_address_by_userid('hw1_user', 'addresses','users',
                                           template)
        return res

    def get_users_by_addressid(template):
        res=d_service.get_users_by_addressid('hw1_user', 'users',
                                           template)
        return res