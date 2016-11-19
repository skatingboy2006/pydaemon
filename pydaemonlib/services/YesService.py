from ServicePeriodical import ServicePeriodical



class YesService(ServicePeriodical):
    def init(self):
        self._timeout = 1


    def handler(self):
        print "yes"
