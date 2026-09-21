program MMArchiveCLI;

{$APPTYPE CONSOLE}

uses
  SysUtils, Classes, Forms, RSUtils, RSSysUtils, RSLod, RSDef, IniFiles;

const
  CLI_VERSION = '1.2.6';

type
  TOperation = (opList, opExtract, opAdd, opHelp, opExtractDef, opVersion);

function CreateDirectoryPath(const Path: string): Boolean;
var
  NormalizedPath: string;
  i: Integer;
  CurrentPath: string;
begin
  Result := True;
  NormalizedPath := StringReplace(Path, '/', '\', [rfReplaceAll]);
  
  if DirectoryExists(NormalizedPath) then
    Exit;
    
  CurrentPath := '';
  i := 1;
  while i <= Length(NormalizedPath) do
  begin
    if NormalizedPath[i] = '\' then
    begin
      if CurrentPath <> '' then
      begin
        if not DirectoryExists(CurrentPath) then
        begin
          if not CreateDir(CurrentPath) then
          begin
            Result := False;
            Exit;
          end;
        end;
      end;
      CurrentPath := CurrentPath + '\';
    end
    else
      CurrentPath := CurrentPath + NormalizedPath[i];
    Inc(i);
  end;
  
  // Create final directory if needed
  if (CurrentPath <> '') and not DirectoryExists(CurrentPath) then
  begin
    if not CreateDir(CurrentPath) then
      Result := False;
  end;
end;

var
  Operation: TOperation;
  ArchivePath: string;
  TargetPath: string;
  OutputPath: string;
  FileFilter: string;
  
  // INI Configuration variables
  ExtractWithShadow: Boolean;
  ExtractIn24Bits: Boolean;
  IgnoreUnzipErrors: Boolean;

procedure LoadConfiguration;
var
  Ini: TIniFile;
  IniPath: string;
begin
  IniPath := ExtractFilePath(ParamStr(0)) + 'MMArchive.ini';
  
  // Set defaults
  ExtractWithShadow := true;
  ExtractIn24Bits := false;
  IgnoreUnzipErrors := false;
  
  try
    Ini := TIniFile.Create(IniPath);
    try
      // Create INI file with defaults if it doesn't exist
      if not FileExists(IniPath) then
      begin
        Ini.WriteBool('General', 'Def Extract With External Shadow', ExtractWithShadow);
        Ini.WriteBool('General', 'Def Extract In 24 Bits', ExtractIn24Bits);
        Ini.WriteBool('General', 'Ignore Unpacking Errors', IgnoreUnzipErrors);
      end
      else
      begin
        ExtractWithShadow := Ini.ReadBool('General', 'Def Extract With External Shadow', true);
        ExtractIn24Bits := Ini.ReadBool('General', 'Def Extract In 24 Bits', false);
        IgnoreUnzipErrors := Ini.ReadBool('General', 'Ignore Unpacking Errors', false);
      end;
    finally
      Ini.Free;
    end;
  except
    // Keep defaults if any error occurs
  end;
end;

procedure ShowHelp;
begin
  WriteLn('MMArchive Command Line Interface');
  WriteLn('Usage:');
  WriteLn('  MMArchiveCLI.exe <operation> <archive> [options]');
  WriteLn;
  WriteLn('Operations:');
  WriteLn('  list <archive>                    - List files in archive');
  WriteLn('  extract <archive> [-o output_dir] [-f *.ext] - Extract files');
  WriteLn('  add <archive> <file>              - Add file to archive');
  WriteLn('  extractdef <archive|def_file> [-o output_dir] - Extract DEF files for DefTool');
  WriteLn('  version                           - Show version information');
  WriteLn('  help                              - Show this help');
  WriteLn;
  WriteLn('Options:');
  WriteLn('  -o <dir>    Output directory');
  WriteLn('  -f <*.ext>  File filter (e.g., *.bmp, *.def)');
  WriteLn;
  WriteLn('Examples:');
  WriteLn('  MMArchiveCLI.exe list data.lod');
  WriteLn('  MMArchiveCLI.exe extract data.lod -o extracted -f *.bmp');
  WriteLn('  MMArchiveCLI.exe add data.lod newfile.txt');
  WriteLn('  MMArchiveCLI.exe extractdef sprites.lod -o deftool');
  WriteLn('  MMArchiveCLI.exe extractdef sprite.def -o deftool');
  WriteLn('  MMArchiveCLI.exe version');
end;

procedure ParseCommandLine;
var
  cmd: string;
  i: Integer;
  param: string;
begin
  Operation := opHelp;
  
  if ParamCount < 1 then
    Exit;
    
  cmd := LowerCase(ParamStr(1));
  
  if cmd = 'help' then
    Operation := opHelp
  else if cmd = 'list' then
  begin
    if ParamCount >= 2 then
    begin
      Operation := opList;
      ArchivePath := ParamStr(2);
    end;
  end
  else if cmd = 'extract' then
  begin
    if ParamCount >= 2 then
    begin
      Operation := opExtract;
      ArchivePath := ParamStr(2);
      OutputPath := ExtractFilePath(ArchivePath) + StringReplace(ExtractFileName(ArchivePath), '.', '_', [rfReplaceAll]) + '\';
      
      i := 3;
      while i <= ParamCount do
      begin
        param := LowerCase(ParamStr(i));
        if param = '-o' then
        begin
          if i + 1 <= ParamCount then
          begin
            OutputPath := ParamStr(i + 1);
            Inc(i, 2);
          end
          else
            Inc(i);
        end
        else if param = '-f' then
        begin
          if i + 1 <= ParamCount then
          begin
            FileFilter := LowerCase(ParamStr(i + 1));
            Inc(i, 2);
          end
          else
            Inc(i);
        end
        else
          Inc(i);
      end;
    end;
  end
  else if cmd = 'add' then
  begin
    if ParamCount >= 3 then
    begin
      Operation := opAdd;
      ArchivePath := ParamStr(2);
      TargetPath := ParamStr(3);
    end;
  end
  else if cmd = 'extractdef' then
  begin
    if ParamCount >= 2 then
    begin
      Operation := opExtractDef;
      ArchivePath := ParamStr(2);
      OutputPath := ExtractFilePath(ArchivePath) + StringReplace(ExtractFileName(ArchivePath), '.', '_', [rfReplaceAll]) + '_deftool\';
      
      i := 3;
      while i <= ParamCount do
      begin
        param := LowerCase(ParamStr(i));
        if param = '-o' then
        begin
          if i + 1 <= ParamCount then
          begin
            OutputPath := ParamStr(i + 1);
            Inc(i, 2);
          end
          else
            Inc(i);
        end
        else
          Inc(i);
      end;
    end;
  end
  else if cmd = 'version' then
    Operation := opVersion;
end;

procedure ListArchive;
var
  Archive: TRSMMArchive;
  i: Integer;
begin
  try
    Archive := RSLoadMMArchive(ArchivePath);
    try
      Archive.RawFiles.IgnoreUnzipErrors := IgnoreUnzipErrors;
      WriteLn('Files in archive: ', Archive.Count);
      WriteLn('Name');
      WriteLn('----');
      for i := 0 to Archive.Count - 1 do
        WriteLn(Archive.Names[i]);
    finally
      Archive.Free;
    end;
  except
    on E: Exception do
    begin
      WriteLn('Error: ', E.Message);
      ExitCode := 1;
    end;
  end;
end;

procedure ExtractArchive;
var
  Archive: TRSMMArchive;
  i, FilteredCount: Integer;
  ExtractedFile: string;
begin
  try
    Archive := RSLoadMMArchive(ArchivePath);
    try
      Archive.RawFiles.IgnoreUnzipErrors := IgnoreUnzipErrors;
      // Count files that match the filter
      FilteredCount := 0;
      for i := 0 to Archive.Count - 1 do
      begin
        if (FileFilter = '') or (Pos(LowerCase(ExtractFileExt(Archive.Names[i])), FileFilter) > 0) then
          Inc(FilteredCount);
      end;
      
      WriteLn('Extracting ', FilteredCount, ' files to: ', OutputPath);
      
      if not CreateDirectoryPath(OutputPath) then
      begin
        WriteLn('Error: Unable to create directory: ', OutputPath);
        ExitCode := 1;
        Exit;
      end;
        
      for i := 0 to Archive.Count - 1 do
      begin
        if (FileFilter = '') or (Pos(LowerCase(ExtractFileExt(Archive.Names[i])), FileFilter) > 0) then
        try
          ExtractedFile := Archive.Extract(i, OutputPath, True);
          if ExtractedFile <> '' then
            WriteLn('Extracted: ', ExtractFileName(ExtractedFile))
          else
            WriteLn('Skipped: ', Archive.Names[i]);
        except
          on E: Exception do
            WriteLn('Error extracting ', Archive.Names[i], ': ', E.Message);
        end;
      end;
      WriteLn('Extraction complete.');
    finally
      Archive.Free;
    end;
  except
    on E: Exception do
    begin
      WriteLn('Error: ', E.Message);
      ExitCode := 1;
    end;
  end;
end;

procedure ExtractForDefTool;
var
  Archive: TRSMMArchive;
  i: Integer;
  ExtractedFile: string;
  DefData: TRSByteArray;
  DefWrapper: TRSDefWrapper;
  FileStream: TFileStream;
begin
  try
    // Check if input is a DEF file or archive
    if SameText(ExtractFileExt(ArchivePath), '.def') then
    begin
      // Handle individual DEF file
      WriteLn('Extracting DEF file for DefTool to: ', OutputPath);
      
      if not CreateDirectoryPath(OutputPath) then
      begin
        WriteLn('Error: Unable to create directory: ', OutputPath);
        ExitCode := 1;
        Exit;
      end;
      
      try
        FileStream := TFileStream.Create(ArchivePath, fmOpenRead);
        try
          SetLength(DefData, FileStream.Size);
          FileStream.ReadBuffer(DefData[0], FileStream.Size);
        finally
          FileStream.Free;
        end;
        
        DefWrapper := TRSDefWrapper.Create(DefData);
        try
          DefWrapper.ExtractDefToolList(IncludeTrailingPathDelimiter(OutputPath) + ChangeFileExt(ExtractFileName(ArchivePath), '.hdl'), ExtractWithShadow, ExtractIn24Bits);
          WriteLn('Extracted DEF: ', ExtractFileName(ArchivePath));
        finally
          DefWrapper.Free;
        end;
      except
        on E: Exception do
        begin
          WriteLn('Error extracting DEF file: ', E.Message);
          ExitCode := 1;
        end;
      end;
    end
    else
    begin
      // Handle archive file
      Archive := RSLoadMMArchive(ArchivePath);
      try
        Archive.RawFiles.IgnoreUnzipErrors := IgnoreUnzipErrors;
        WriteLn('Extracting DEF files for DefTool to: ', OutputPath);
        
        if not CreateDirectoryPath(OutputPath) then
        begin
          WriteLn('Error: Unable to create directory: ', OutputPath);
          ExitCode := 1;
          Exit;
        end;
          
        for i := 0 to Archive.Count - 1 do
        begin
          if SameText(ExtractFileExt(Archive.Names[i]), '.def') then
          try
            ExtractedFile := IncludeTrailingPathDelimiter(OutputPath) + ChangeFileExt(Archive.Names[i], '') + '\';
            if not ForceDirectories(ExtractedFile) then
            begin
              WriteLn('Error creating directory: ', ExtractedFile);
              continue;
            end;
            
            Archive.ExtractArrayOrBmp(i, DefData).Free;
            
            DefWrapper := TRSDefWrapper.Create(DefData);
            try
            DefWrapper.ExtractDefToolList(ExtractedFile + ChangeFileExt(Archive.Names[i], '.hdl'), ExtractWithShadow, ExtractIn24Bits);
            WriteLn('Extracted DEF: ', Archive.Names[i]);
          finally
            DefWrapper.Free;
          end;
        except
          on E: Exception do
            WriteLn('Error extracting ', Archive.Names[i], ': ', E.Message);
        end;
      end;
      WriteLn('DEF extraction complete.');
    finally
      Archive.Free;
    end;
    end;
  except
    on E: Exception do
    begin
      WriteLn('Error: ', E.Message);
      ExitCode := 1;
    end;
  end;
end;

procedure AddToArchive;
var
  Archive: TRSMMArchive;
  FileStream: TFileStream;
  FileName: string;
begin
  try
    if not FileExists(ArchivePath) then
    begin
      WriteLn('Archive not found: ', ArchivePath);
      ExitCode := 1;
      Exit;
    end;
    
    if not FileExists(TargetPath) then
    begin
      WriteLn('File not found: ', TargetPath);
      ExitCode := 1;
      Exit;
    end;
    
    Archive := RSLoadMMArchive(ArchivePath);
    try
      Archive.RawFiles.IgnoreUnzipErrors := IgnoreUnzipErrors;
      FileStream := TFileStream.Create(TargetPath, fmOpenRead);
      try
        FileName := ExtractFileName(TargetPath);
        Archive.Add(FileName, FileStream);
        WriteLn('Added: ', FileName);
      finally
        FileStream.Free;
      end;
      
      Archive.SaveAs(ArchivePath);
      WriteLn('Archive saved.');
    finally
      Archive.Free;
    end;
  except
    on E: Exception do
    begin
      WriteLn('Error: ', E.Message);
      ExitCode := 1;
    end;
  end;
end;

begin
  try
    LoadConfiguration;
    ParseCommandLine;
    
    case Operation of
      opHelp: ShowHelp;
      opList: 
      begin
        if not FileExists(ArchivePath) then
        begin
          WriteLn('Archive not found: ', ArchivePath);
          ExitCode := 1;
        end
        else
          ListArchive;
      end;
      opExtract:
      begin
        if not FileExists(ArchivePath) then
        begin
          WriteLn('Archive not found: ', ArchivePath);
          ExitCode := 1;
        end
        else
          ExtractArchive;
      end;
      opAdd: AddToArchive;
      opExtractDef:
      begin
        if not FileExists(ArchivePath) then
        begin
          WriteLn('Archive not found: ', ArchivePath);
          ExitCode := 1;
        end
        else
          ExtractForDefTool;
      end;
      opVersion:
      begin
        WriteLn('MMArchive CLI Version ', CLI_VERSION);
        WriteLn('Based on MMArchive by GrayFace');
      end;
    end;
  except
    on E: Exception do
    begin
      WriteLn('Unexpected error: ', E.Message);
      ExitCode := 1;
    end;
  end;
end.