import database_services.RDBService as d_service


class UserResource():

    def __init__(self):
        pass

    def get_user_by_template(template):
        res = d_service.find_by_template('hw1_user', 'users',
                                       template, None)
        return res

    def post_user_by_template(template):
        res = d_service.insert_by_template('hw1_user', 'users',
                                         template,None)
        return res

    def put_user_by_id(template,id):
        res = d_service.update_by_id('hw1_user', 'users',
                                         template,id)
        return res

    def delete_user_by_id(id):
        res = d_service.delete_by_id('hw1_user', 'users',
                                           id)
        return res