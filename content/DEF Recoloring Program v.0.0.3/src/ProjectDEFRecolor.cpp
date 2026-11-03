//---------------------------------------------------------------------------

#include <vcl.h>
#pragma hdrstop
USERES("ProjectDEFRecolor.res");
USEFORM("Unit1.cpp", FormRecolor);
//---------------------------------------------------------------------------
WINAPI WinMain(HINSTANCE, HINSTANCE, LPSTR, int)
{
        try
        {
                 Application->Initialize();
                 Application->CreateForm(__classid(TFormRecolor), &FormRecolor);
                 Application->Run();
        }
        catch (Exception &exception)
        {
                 Application->ShowException(&exception);
        }
        return 0;
}
//---------------------------------------------------------------------------
