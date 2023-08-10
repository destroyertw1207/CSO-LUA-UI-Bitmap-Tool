
def exportColorData(var, data):
    export_data = data
    export_var = var + "_data"
    export_demo = f"{var} = Bitmap:Create({export_var})\n"
    export_demo += f"{var}:Set(100, 100, 200, 200, 1)\n\n"

    return export_data + export_demo

def exprotMinifyClass():
    return 'local function a(b,c)for d in pairs(b)do if type(b[d])==type(c[d])then if type(b[d])=="table"then a(b[d],c[d])else b[d]=c[d]end end end end;local function e(f,g,c)for h,i in pairs(f)do if type(i)=="table"then e(i,g)elseif type(i)=="userdata"then i[g](i,c)end end end;local function j(f)local k={}for d,i in pairs(f)do if type(i)=="table"then k[d]=j(i)else k[d]=i end end;return k end;Bitmap={}Bitmap.__index=Bitmap;function Bitmap:Set(l,m,n,o,p)self.SetArg.x=l or self.SetArg.x;self.SetArg.y=m or self.SetArg.y;self.SetArg.width=n or self.SetArg.width;self.SetArg.height=o or self.SetArg.height;self.SetArg.spacing=p or self.SetArg.spacing;self:Update()end;function Bitmap:Get()return j(self.SetArg)end;function Bitmap:Show()e(self.UI,"Show")self.visible=true end;function Bitmap:Hide()e(self.UI,"Hide")self.visible=false end;function Bitmap:IsVisible()return self.visible end;function Bitmap:Create(q)local b={SetArg={x=0,y=0,width=0,height=0,spacing=0},row_count=nil,column_count=nil,pixelColorData=q,visible=true,UI={}}b.row_count=#b.pixelColorData;b.column_count=#b.pixelColorData[1]for r=1,b.row_count do b.UI[r]={}for s=1,b.column_count do b.UI[r][s]=nil end end;return setmetatable(b,self)end;function Bitmap:Update()local t=self.SetArg;local l=t.x;local m=t.y;local u=math.floor(t.width/self.row_count)local v=math.floor(t.height/self.column_count)local w=self.pixelColorData;local p=t.spacing;local x=l;local y=m;for z=1,self.row_count do for A=1,self.column_count do local B=w[z][A]if not(B[4]==0)then if not self.UI[z][A]then self.UI[z][A]=UI.Box.Create()end;self.UI[z][A]:Set({x=x,y=y,width=u,height=v,r=B[1],g=B[2],b=B[3],a=B[4]})end;x=x+u+p end;x=l;y=y+v+p end end'

def exportClass():
    return """------------------------------------
--[[ functions ]]
------------------------------------

local function setArgs(data, args)
    for k in pairs(data) do
        if type(data[k]) == type(args[k]) then
            if type(data[k]) == "table" then
                setArgs(data[k], args[k])
            else
                data[k] = args[k]
            end
        end
    end
end

local function deepCall(table, funcName, args)
    for _,v in pairs(table) do
        if type(v) == "table" then
            deepCall(v, funcName)
        elseif type(v) == "userdata" then
            v[funcName](v, args)
        end
    end
end

local function clone(table)
    local temp = {}
    for k,v in pairs(table) do
        if type(v) == "table" then
            temp[k] = clone(v)
        else
            temp[k] = v
        end
    end
    return temp
end

------------------------------------
--[[ Bitmap Class ]]
------------------------------------

Bitmap = {}
Bitmap.__index = Bitmap

function Bitmap:Set(x, y, w, h, spacing)
    self.SetArg.x = x or self.SetArg.x
    self.SetArg.y = y or self.SetArg.y
    self.SetArg.width = w or self.SetArg.width
    self.SetArg.height = h or self.SetArg.height
    self.SetArg.spacing = spacing or self.SetArg.spacing
    
    self:Update()
end


function Bitmap:Get()
    return clone(self.SetArg)
end
    
    
function Bitmap:Show()
    deepCall(self.UI, "Show")
    self.visible = true
end


function Bitmap:Hide()
    deepCall(self.UI, "Hide")
    self.visible = false
end


function Bitmap:IsVisible()
    return self.visible
end


function Bitmap:Create(pixelColorData)
    local data = {
        SetArg = {
            x = 0,
            y = 0,
            width = 0,
            height = 0,
            spacing = 0
        },
        row_count = nil,
        column_count = nil,
        pixelColorData = pixelColorData,
        visible = true,
        UI = {}
    }
    
    data.row_count = #data.pixelColorData
    data.column_count = #data.pixelColorData[1]
    
    for i = 1, data.row_count do
        data.UI[i] = {}
        for j = 1, data.column_count do
            data.UI[i][j] = nil
        end
    end
    
    return setmetatable(data, self)
end


function Bitmap:Update()
    local arg = self.SetArg
    local x = arg.x
    local y = arg.y
    local boxWidth = math.floor(arg.width / self.row_count)
    local boxHeight = math.floor(arg.height / self.column_count)
    local colors = self.pixelColorData
    local spacing = arg.spacing
    
    local currX = x
    local currY = y
    
    for row = 1, self.row_count do
        for column = 1, self.column_count do
            local color = colors[row][column]
            
            if not (color[4] == 0) then
                if not self.UI[row][column] then
                    self.UI[row][column] = UI.Box.Create()
                end
                self.UI[row][column]:Set({
                    x = currX,
                    y = currY,
                    width = boxWidth,
                    height = boxHeight,
                    r = color[1],
                    g = color[2],
                    b = color[3],
                    a = color[4]
                })
            end
            
            currX = currX + boxWidth + spacing
        end
        currX = x
        currY = currY + boxHeight + spacing
    end
end"""
