class KeyWords:
    def __init__(self):
        self.title=['汇报主题:','报告主题:','学术报告:','标题:','报告题目','题目','Title:']
        self.speaker=['汇报人:','报告人:','Speaker','主讲人:','演讲人:','报告专家']
        self.venue=['地点:','Venue','venue','Place:','Address']
        self.time=['时间:','Time:']

    def set_title(self,title):
        if title not in self.title:
            self.title.append(title)

    def set_speaker(self,speaker):
        if speaker not in self.speaker:
           self.speaker.append(speaker)

    def set_venue(self,venue):
        if venue not in self.venue:
            self.venue.append(venue)

    def set_time(self,time):
        if time not in self.time:
            self.time.append(time)
