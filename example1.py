
import b3
import time

class CAtkCondition(b3.Condition):
    def tick(self,tick):
        target=tick.target
        if target.validattack():
            return b3.SUCCESS
        return b3.FAILURE

class CAtkAction(b3.Action):
    def tick(self,tick):
        target=tick.target
        if target.attack():
            return b3.RUNNING
        return b3.SUCCESS

class CEatCondition(b3.Condition):
    def tick(self,tick):
        target=tick.target
        if target.valideat():
            return b3.SUCCESS
        return b3.FAILURE

class CEatAction(b3.Action):
    def tick(self,tick):
        target=tick.target
        if target.eat():
            return b3.RUNNING
        return b3.SUCCESS

class CSleepCondition(b3.Condition):
    def tick(self,tick):
        target=tick.target
        if target.validsleep():
            return b3.SUCCESS
        return b3.FAILURE

class CSleepAction(b3.Action):
    def tick(self,tick):
        target=tick.target
        if target.sleep():
            return b3.RUNNING
        return b3.SUCCESS

class CSelector(b3.Priority):
    def __init__(self):
        atkseq=b3.Sequence([CAtkCondition(),CAtkAction()])
        eatseq=b3.Sequence([CEatCondition(),CEatAction()])
        sleepseq=b3.Sequence([CSleepCondition(),CSleepAction()])
        childlist=[atkseq,eatseq,sleepseq]
        super(CSelector,self).__init__(childlist)

class CAITarget(object):
    def __init__(self,iTargetID):
        self.m_ID=iTargetID
        self.m_HP=100
        self.m_MP=100
        self.m_EatBeginTime=0
        self.m_SleepBeginTime=0

    def validattack(self):
        if self.m_HP>0 and self.m_MP>0:
            return True
        return False

    def attack(self):
        print "attack"
        self.m_HP-=20
        self.m_MP-=10
        if self.validattack():
            return True
        return False

    def valideat(self):
        if self.m_HP<=0:
            return True
        return False

    def eat(self):
        print "eat"
        if not self.m_EatBeginTime:
            self.m_EatBeginTime=int(time.clock())
        iNowTime=int(time.clock())
        if iNowTime-self.m_EatBeginTime>=2:
            self.m_HP=100
            self.m_EatBeginTime=0
            return False
        return True

    def validsleep(self):
        if self.m_MP<=0:
            return True
        return False

    def sleep(self):
        print "sleep"
        if not self.m_SleepBeginTime:
            self.m_SleepBeginTime=int(time.clock())
        iNowTime=int(time.clock())
        if iNowTime-self.m_SleepBeginTime>=4:
            self.m_MP=100
            self.m_SleepBeginTime=0
            return False
        return True

tree=b3.BehaviorTree()
bb=b3.Blackboard()
aitarget=CAITarget(1001)
tree.root=CSelector()
iBegin=int(time.clock())
iLastTime=int(time.clock())
while iLastTime-iBegin<100:
    tree.tick(aitarget,bb)
    iLastTime=int(time.clock())
    time.sleep(0.5)


