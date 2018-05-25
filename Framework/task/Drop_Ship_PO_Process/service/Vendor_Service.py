from task.Drop_Ship_PO_Process.db.Mapping import DBSession, VendorInfo


class VendorService(object):
    @staticmethod
    def get_vendors(vendor=None, bu=None, browser=None, ip_address=None):
        session = DBSession()
        query = session.query(VendorInfo)

        if vendor is not None:
            query = query.filter_by(vendor=vendor)
        if bu is not None:
            query = query.filter_by(bu=bu)
        if browser is not None:
            query = query.filter_by(browser=browser)
        if ip_address is not None:
            query = query.filter_by(ip_address=ip_address)

        return query.all()

