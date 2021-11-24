class polyDict:
    def __init__(self,axii=["key","value"],data=[]):#data = [{"key": 5,"value": 10}] and use non-axii for non-access ones
        self.stored = {hash(str(d)):d for d in data}
        self.refs = {axis:{str(data[i][axis]):hash(str(data[i])) for i in range(len(data))} for axis in axii}
        #speed var
        self.len = len(self.stored)
    
    def __len__(self):
        return self.len
    
    def __str__(self):
        return "axii: "+str([i for i in self.refs.keys()])+"\n"+"\n".join(["poly ID "+str(i[0])+": "+str(i[1]) for i in self.stored.items()])
    
    def criteriaID(self,criteria):
        for id,data in self.stored.items():
            keys = [i for i in data.keys()]
            
            i=0
            
            for s in range(len(keys)):#clean out non-criteria checks
                if not keys[i] in [i for i in criteria.keys()]:
                    del keys[i]
                    i-=1
                i+=1
            i=0
            
            if len(keys)!=0:
                continue
            
            for s in range(len(keys)):
                if not data[keys[i]]==criteria[keys[i]]:#make sure each check is true, if yes return it
                    break
                i+=1
            if i==len(criteria)-1:
                return id
        
        return 0.1
    
    def set(self, set, criteria={}):#turns into add element by default
        if criteria!={}:
            id = self.criteriaID(criteria)
            if id!=0.1:
                for k,v in set.items():
                    self.stored[id][k] = v
                return
        
        for axis in set.keys():
            if axis in self.refs.keys():
                self.refs[axis][str(set[axis])]=len(self.stored)
        
        self.stored[hash(str(set))]=set
        self.len = len(self.stored)
        
        
    def get(self, criteria):
        assert type(criteria)==dict
        id = self.criteriaID(criteria)
        if id==.1:
            raise KeyError("Could not find poly with criteria "+str(criteria))
        return self.stored[id]
    
    def rem(self,criteria):
        id = self.criteriaID(criteria)
        if id!=.1:
            del self.stored[id]
            for axis in self.refs.keys():
                if id in self.refs[axis].values() and axis in criteria.keys():
                    del self.refs[axis][str(criteria[axis])]
            self.len = len(self.stored)

if __name__ == "__main__":
    pd = polyDict(data=[{"key":1,"value":100},{"key":3,"value":300}])
    print(pd)
    print(pd.refs)
    pd.set({"socks":4},criteria={"key":1})
    print(pd)
    pd.set({"socks":22,"babushka": "three","key":200})
    print(pd)
    pd.set({"socks":5},criteria={"key":200})
    print(pd)
    pd.rem({"key":1})
    print(pd)
    pd.rem({"key":3})
    print(pd)