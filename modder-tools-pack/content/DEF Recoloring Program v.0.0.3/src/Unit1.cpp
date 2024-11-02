//---------------------------------------------------------------------------
#include <fstream>

#include <vcl.h>
#include <iostream.h>
#pragma hdrstop
#include <stdio.h>
#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TFormRecolor *FormRecolor;
 int ColorsCorrected[256];
//---------------------------------------------------------------------------
__fastcall TFormRecolor::TFormRecolor(TComponent* Owner)
        : TForm(Owner)
{
for(int t=0;t<256;t++)
        {
         ComboBoxTreshold->Items->Add(IntToStr(t));
         ColorsCorrected[t]=0;
        }
  ComboBoxTreshold->ItemIndex=0;

}
//---------------------------------------------------------------------------
 AnsiString inFile;
 FILE *inFileH;
 AnsiString outFile;
   int sizeBuf;
 char *buffer,*bufferOut ;
 char *bufferPalettes;
 struct rgb{
     int r;
     int g;
     int b;

 };


            TButton *ButtonIn[256];
            TButton *ButtonOut[256];
 rgb ColorIn[256];
 rgb ColorOut[256];
  rgb ColorInReplace[256];
 rgb ColorOutReplace[256];
void __fastcall TFormRecolor::ButtonOpenDEFClick(TObject *Sender)
{
ButtonOpenDEF->Enabled=false;
        ButtonSaveInPalette->Enabled=false;
      ButtonSaveOutPalette->Enabled=false;
      ButtonLoadOutPalette->Enabled=false;
      ButtonSaveDEFFile->Enabled=false;
      ButtonLoadPrevInPalette->Enabled=false;
      ButtonPrevOutPalette->Enabled=false;
if(OpenDialog1->Execute())
   {
   if(buffer) {free(buffer);}
      if(bufferOut) {free(bufferOut);}
 //  if(buffer) delete buffer;
 //     if(bufferOut) delete bufferOut;
   outFile="";
   inFile="";

   inFile=OpenDialog1->FileName;
   LabelDEFFile->Caption=inFile;
   inFileH = fopen(inFile.c_str(),"rb");
   if(inFileH)
    {
      int fsize;
        fseek(inFileH, 0, SEEK_END);
 fsize=ftell(inFileH);
 sizeBuf=   fsize;
// if(buffer) {delete buffer;}
//  if(bufferOut) {delete bufferOut;}
      buffer = (char*)malloc(fsize);
       bufferOut = (char*)malloc(fsize);
      fseek(inFileH, SEEK_SET, 0);
      fread(buffer,fsize,1,inFileH);
      for(int i=0;i<sizeBuf;i=i+1)
          {
          bufferOut[i]=buffer[i];
          }

         fclose(inFileH);
      for(int i=0;i<256;i=i+1)
        {
           ColorIn[i].r=0xFF&(buffer[16+i*3]);
           ColorIn[i].g=0xFF&(256+(buffer[17+i*3]));
           ColorIn[i].b=0xFF&(256+(buffer[18+i*3]));

           ColorOut[i].r=0xFF&(buffer[16+i*3]);
           ColorOut[i].g=0xFF&(256+(buffer[17+i*3]));
           ColorOut[i].b=0xFF&(256+(buffer[18+i*3]));
           AnsiString nameShape="Shape"+IntToStr((i)+1);
   //        TButton * Buttonlnstance = FindComponent(nameShape);
          TShape *Buttonlnstance = (TShape *)FindComponent(nameShape);
          TColor col= (TColor)RGB(ColorIn[i].r, ColorIn[i].g, ColorIn[i].b);
          Buttonlnstance->Brush->Color = col;
           Buttonlnstance->Hint="RGB ("+IntToStr(ColorIn[i].r)+","+ColorIn[i].g+","+ColorIn[i].b+")";
           nameShape="Shape"+IntToStr(256+(i)+1);
           Buttonlnstance = (TShape *)FindComponent(nameShape);
           Buttonlnstance->Brush->Color = col;
            Buttonlnstance->Hint="RGB ("+IntToStr(ColorIn[i].r)+","+ColorIn[i].g+","+ColorIn[i].b+")";

            Buttonlnstance->OnMouseUp=clickShapeEvent;


        }

       ButtonOpenDEF->Enabled=false;
      ButtonSaveInPalette->Enabled=true;
      ButtonSaveOutPalette->Enabled=true;
      ButtonLoadOutPalette->Enabled=true;
      ButtonSaveDEFFile->Enabled=true;
       ButtonLoadPrevInPalette->Enabled=true;

   }

   }
}
//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
   void __fastcall TFormRecolor::clickShapeEvent(TObject *Sender,
      TMouseButton Button, TShiftState Shift, int X, int Y)
   {
        if(CheckBoxColors->Checked==false)
        ColorDialog1->Color= ((TShape*)Sender)->Brush->Color;
        if( ColorDialog1->Execute())
        {
           ((TShape*)Sender)->Brush->Color=ColorDialog1->Color;

        }

   }


void __fastcall TFormRecolor::ButtonSaveInPaletteClick(TObject *Sender)
{    //save in palette
  if(SaveDialog3->Execute())
   {
   AnsiString inpal=SaveDialog3->FileName;
   FILE *outpal = fopen(inpal.c_str(),"wb");
   if(outpal)
   {
         for(int i=0;i<256;i++)
        {



          fwrite( &ColorIn[i].r,1,1,outpal);
          fwrite( &ColorIn[i].g,1,1,outpal);
          fwrite(  &ColorIn[i].b,1,1,outpal);
        }
   }
   fclose(outpal);
}    }
//---------------------------------------------------------------------------

void __fastcall TFormRecolor::ButtonLoadOutPaletteClick(TObject *Sender)
{   //load out palette
  if(OpenDialog2->Execute())
   {
   AnsiString inpalf=OpenDialog2->FileName;
   FILE *inpal = fopen(inpalf.c_str(),"rb");
   if(inpal)
   {

      fread(bufferOut+16,256*3,1,inpal);
              fclose(inpal);
          for(int i=0;i<256;i++)
        {


                     ColorOut[i].r=0xFF&(bufferOut[16+i*3]);
           ColorOut[i].g=0xFF&(256+(bufferOut[17+i*3]));
           ColorOut[i].b=0xFF&(256+(bufferOut[18+i*3]));

                           AnsiString nameShape="Shape"+IntToStr(256+(i)+1);
   //        TButton * Buttonlnstance = FindComponent(nameShape);
          TShape *Buttonlnstance = (TShape *)FindComponent(nameShape);
          TColor col= (TColor)RGB(ColorOut[i].r, ColorOut[i].g, ColorOut[i].b);
          Buttonlnstance->Brush->Color = col;

        }

   }
     }
}
//---------------------------------------------------------------------------

void __fastcall TFormRecolor::ButtonSaveOutPaletteClick(TObject *Sender)
{     //save out palette
   if(SaveDialog3->Execute())
   {
   AnsiString inpal=SaveDialog3->FileName;
   FILE *outpal = fopen(inpal.c_str(),"wb");
   if(outpal)
   {
        for(int i=0;i<256;i++)
        {
        AnsiString nameShape="Shape"+IntToStr(256+i+1);
           TShape *Buttonlnstance = (TShape *)FindComponent(nameShape);
           TColor col=Buttonlnstance->Brush->Color ;


             ColorOut[i].b=((col&0xFF0000)/256/256);
             ColorOut[i].g=((col&0x00FF00))/256;
             ColorOut[i].r=(col&0x0000FF);

          bufferOut[16+i*3]=(char)ColorOut[i].r;
          bufferOut[17+i*3]=(char)ColorOut[i].g;
          bufferOut[18+i*3]=(char)ColorOut[i].b;


        }
            fwrite(bufferOut+16,256*3,1,outpal);
           fclose(outpal);
   }

}
}
//---------------------------------------------------------------------------

void __fastcall TFormRecolor::ButtonSaveDEFFileClick(TObject *Sender)
{

   //Save DEF
if(SaveDialog1->Execute())
   {
   AnsiString inpalf=SaveDialog1->FileName;
      FILE *inpal = fopen(inpalf.c_str(),"wb");
      if(inpal)
      {

         for(int t=0;t<sizeBuf;t++)
         {
         bufferOut[t]=buffer[t];
         }


        for(int i=0;i<256;i++)
        {
        AnsiString nameShape="Shape"+IntToStr(256+i+1);
           TShape *Buttonlnstance = (TShape *)FindComponent(nameShape);
           TColor col=Buttonlnstance->Brush->Color ;


             ColorOut[i].b=((col&0xFF0000)/256/256);
             ColorOut[i].g=((col&0x00FF00))/256;
             ColorOut[i].r=(col&0x0000FF);

          bufferOut[16+i*3]=(char)ColorOut[i].r;
          bufferOut[17+i*3]=(char)ColorOut[i].g;
          bufferOut[18+i*3]=(char)ColorOut[i].b;


        }
            fwrite(bufferOut,sizeBuf,1,inpal);
            fclose(inpal);
      }

   }

}
//---------------------------------------------------------------------------




void __fastcall TFormRecolor::ButtonLoadPrevInPaletteClick(TObject *Sender)
{
  if(OpenDialog2->Execute())
   {
   AnsiString inpalf=OpenDialog2->FileName;
   FILE *inpal = fopen(inpalf.c_str(),"rb");
   if(inpal)
   {
        char bufferPalettes[256*3];
      fread(bufferPalettes,256*3,1,inpal);
              fclose(inpal);
          for(int i=0;i<256;i++)
        {


           ColorInReplace[i].r=0xFF&(bufferPalettes[i*3]);
           ColorInReplace[i].g=0xFF&(256+(bufferPalettes[1+i*3]));
           ColorInReplace[i].b=0xFF&(256+(bufferPalettes[2+i*3]));

        }
        ButtonPrevOutPalette->Enabled=true;
   }
     }
}
//---------------------------------------------------------------------------

void __fastcall TFormRecolor::ButtonPrevOutPaletteClick(TObject *Sender)
{
  if(OpenDialog2->Execute())
   {
   AnsiString inpalf=OpenDialog2->FileName;
   FILE *inpal = fopen(inpalf.c_str(),"rb");
   if(inpal)
   {
        char bufferPalettes[256*3];
      fread(bufferPalettes,256*3,1,inpal);
              fclose(inpal);
          for(int i=0;i<256;i++)
        {


           ColorOutReplace[i].r=0xFF&(bufferPalettes[i*3]);
           ColorOutReplace[i].g=0xFF&(256+(bufferPalettes[1+i*3]));
           ColorOutReplace[i].b=0xFF&(256+(bufferPalettes[2+i*3]));

        }
        ButtonReplaceColors->Enabled=true;
        ComboBoxTreshold->Enabled=true;
            for(int t=0;t<256;t++)
        {

         ColorsCorrected[t]=0;
        }


   }
     }
}
//---------------------------------------------------------------------------
bool comparePoints(struct rgb In1,struct rgb In2,int treshold)
{

int radius= sqrt(pow((In1.r-In2.r),2)+pow((In1.g-In2.g),2)+pow((In1.b-In2.b),2));



                if((In1.r==In2.r)&&
                (In1.g==In2.g)&&
                (In1.b==In2.b)
                ||
                ((treshold>0)&&(radius<=treshold))
                )
                return true;
                else return false;



}



void __fastcall TFormRecolor::ButtonReplaceColorsClick(TObject *Sender)
{
ComboBoxTreshold->Enabled=false;
int treshold= StrToInt(ComboBoxTreshold->Items->Strings[ComboBoxTreshold->ItemIndex]);






        for(int i=8;i<256;i++)
        {
          for(int ind=8;ind<256;ind++)
           {
           if(ColorsCorrected[ind]==0)
           {
           if(    (((i==8)||(i==255))&&(comparePoints(ColorIn[ind],ColorInReplace[i],treshold))    ||
                (comparePoints(ColorIn[ind-1],ColorInReplace[i-1],treshold)&&comparePoints(ColorIn[ind],ColorInReplace[i],treshold)&&comparePoints(ColorIn[ind+1],ColorInReplace[i+1],treshold))
              ))
                   {

                        ColorOut[ind].r=ColorOutReplace[i].r;
                        ColorOut[ind].g=ColorOutReplace[i].g;
                        ColorOut[ind].b=ColorOutReplace[i].b;
                        ColorsCorrected[ind]=1;
                        AnsiString nameShape="Shape"+IntToStr(256+(i)+1);
   //        TButton * Buttonlnstance = FindComponent(nameShape);
                        TShape *Buttonlnstance = (TShape *)FindComponent(nameShape);
                        TColor col= (TColor)RGB(ColorOutReplace[ind].r, ColorOutReplace[ind].g, ColorOutReplace[ind].b);
                        Buttonlnstance->Brush->Color = col;
                        }

                   }

           }
        }


 ComboBoxTreshold->Enabled=true;

}
//---------------------------------------------------------------------------

void __fastcall TFormRecolor::ButtonQuitClick(TObject *Sender)
{
this->Close();
}
//---------------------------------------------------------------------------


