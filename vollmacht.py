from fastapi import  FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz
import datetime



app = FastAPI()
origins = [
    "http://kinderkulturverein.de",
    "https://kinderkulturverein.de",
    "http://www.kinderkulturverein.de",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def pdf(name,strasse,plz,ort,land,datum,sprache):
    if sprache=="de":
        fn="Vollmacht ACCEPT EINS deutsch.pdf"
    elif sprache=="en":
        fn="Vollmacht_ACCEPT EINS deutsch-englisch.pdf"
    elif sprache=="de1":
        fn="Vollmacht Geller deutsch.pdf"
    elif sprache=="en1":
        fn="Vollmacht_Geller deutsch-englisch.pdf"
    else:
        fn=""
    doc=fitz.open(fn)

    z=[name,strasse,plz,ort,land]

    page=doc[0]
    adresse=page.searchFor('Vollmachtgeber')[0]
    x0=adresse[0]
    y0=adresse[3]
    r1=fitz.Rect(x0,y0+10,x0+250,y0+80)
    berlin=page.searchFor('Berlin')[-1]
    x1=berlin[2]
    y1=berlin[1]
    r2=fitz.Rect(x1+10,y1,x1+100,y1+14)
    
    shape=page.newShape()
    shape.drawRect(r1)
    shape.drawRect(r2)
    shape.finish(width=0.1,color=(1,1,1),fill=(1,1,1))
    rc=shape.insertTextbox(r1,z[0]+'\n'+z[1]+'\n'+z[2]+' '+z[3]+'\n'+z[4],color=(0,0,0),fontname='tibo',fontsize=14)
    rc=shape.insertTextbox(r2,datum,color=(0,0,0),fontname='tiro',fontsize=14)
    
    shape.commit()
    doc.save('Vollmacht1.pdf')
    
    


@app.get("/vollmacht/")
async def vollmacht(name:str,strasse:str,plz:str,ort:str="Berlin",land:str="",sprache:str="de"):
    heute=datetime.date.today().strftime("%d.%m.%Y")
    data = pdf(name,strasse,plz,ort,land,heute,sprache)
    return  FileResponse('Vollmacht1.pdf')   #{"name": name,"str":strasse,"ort":plzort}