class KonversiChoice:
    
    def gender(self,no):
        konvert={
            "PRIA" : 1,
            "WANITA" : 2
        }

        return konvert[no]
    
    def religion(self,no):
        konvert={
            "ISLAM" : 1,
            "KRISTEN" : 2,
            "KATHOLIK" : 3,
            "HINDU" : 4,
            "BUDDHA" : 5,
            "OTHER_RELIGION" : 6
        }

        return konvert[no]
    
    def status(self,no):
        konvert={
            "ACTIVE" : 1,
            "TERMINATE" : 2,
            "RESIGN" : 3,
            "ALUMNI" : 4,
            "OTHER_STAFF_STATUS" : 5
        }

        return konvert[no]
    
    def levels(self,no):
        konvert = {
            "DIREKTUR" : 1,
            "WAKIL_DIREKTUR" : 2,
            "KOORDINATOR_ASISTEN" : 3,
            "KEPALA_DIVISI" : 4,
            "STAFF" : 5
        }

        return konvert[no]
    