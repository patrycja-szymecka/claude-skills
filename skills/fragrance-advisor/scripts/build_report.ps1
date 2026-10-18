# Builds the interactive report from a filled template (Windows, no Python needed).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_report.ps1 -Src work\portret-x.html -Out work\portret-x.built.html
# 1. Downloads missing Fragrantica images for every {{IMG_id}}, {{NOTE_id}}, {{BOT_id}} in -Src into -Cache.
# 2. Makes one-colour burgundy note icons (eng\<id>.png) and botanical plates (bot\<id>.jpg).
# 3. Embeds everything as data: URIs and writes a full page (-Out) plus, with -Artifact, a skeleton-free copy for the Artifact tool.
param(
  [Parameter(Mandatory)][string]$Src,
  [Parameter(Mandatory)][string]$Out,
  [string]$Artifact,
  [string]$Cache = "$PSScriptRoot\..\work\img"
)
$ErrorActionPreference = 'Stop'
foreach ($d in 'notes','eng','bot') { New-Item -ItemType Directory -Force "$Cache\$d" | Out-Null }
$c = [IO.File]::ReadAllText((Resolve-Path $Src))

function Get-Img($url, $dst) {
  if (Test-Path $dst) { return }
  for ($try = 0; $try -lt 4; $try++) {
    try { Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $dst -Headers @{ Referer = 'https://www.fragrantica.com/' } -UserAgent 'Mozilla/5.0'; return }
    catch { Start-Sleep -Seconds (2 + 2 * $try) }
  }
  throw "Could not download $url"
}
$bottles = [regex]::Matches($c, '\{\{IMG_(\d+)\}\}') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$notes   = [regex]::Matches($c, '\{\{(NOTE|BOT)_(\d+)\}\}') | ForEach-Object { $_.Groups[2].Value } | Sort-Object -Unique
$bots    = [regex]::Matches($c, '\{\{BOT_(\d+)\}\}') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($id in $bottles) { Get-Img "https://fimgs.net/mdimg/perfume/375x500.$id.jpg" "$Cache\$id.jpg"; Start-Sleep -Milliseconds 400 }
foreach ($id in $notes)   { Get-Img "https://fimgs.net/mdimg/sastojci/o.$id.jpg" "$Cache\notes\$id.jpg"; Start-Sleep -Milliseconds 400 }

if (-not ('Botanical3' -as [type])) {
  Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @"
using System; using System.Drawing; using System.Drawing.Imaging; using System.Runtime.InteropServices;
public static class Engrave3 {
  public static void Run(string src, string dst, int size, int r, int g, int b, double lineGain, double toneMax) {
    using (var im0 = new Bitmap(src)) using (var im = new Bitmap(im0, new Size(size, size))) {
      int w = size, h = size; var L = new double[w*h];
      var d = im.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
      var buf = new byte[w*h*4]; Marshal.Copy(d.Scan0, buf, 0, buf.Length); im.UnlockBits(d);
      for (int i=0;i<w*h;i++) L[i] = (0.299*buf[i*4+2] + 0.587*buf[i*4+1] + 0.114*buf[i*4]) / 255.0;
      var B = new double[w*h];
      for (int y=0;y<h;y++) for (int x=0;x<w;x++) { double s=0; int c=0; for(int j=-1;j<=1;j++) for(int k=-1;k<=1;k++){ int yy=y+j, xx=x+k; if(yy<0||yy>=h||xx<0||xx>=w) continue; s+=L[yy*w+xx]; c++; } B[y*w+x]=s/c; }
      var outb = new byte[w*h*4];
      for (int y=1;y<h-1;y++) for (int x=1;x<w-1;x++) {
        double gx = -B[(y-1)*w+x-1]-2*B[y*w+x-1]-B[(y+1)*w+x-1]+B[(y-1)*w+x+1]+2*B[y*w+x+1]+B[(y+1)*w+x+1];
        double gy = -B[(y-1)*w+x-1]-2*B[(y-1)*w+x]-B[(y-1)*w+x+1]+B[(y+1)*w+x-1]+2*B[(y+1)*w+x]+B[(y+1)*w+x+1];
        double e = Math.Min(1, Math.Sqrt(gx*gx+gy*gy) * lineGain);
        double t = Math.Pow(1 - B[y*w+x], 1.3) * toneMax;
        double a = 1 - (1-e)*(1-t);
        int i = (y*w+x)*4; outb[i]=(byte)b; outb[i+1]=(byte)g; outb[i+2]=(byte)r; outb[i+3]=(byte)Math.Round(a*255);
      }
      using (var o = new Bitmap(w,h,PixelFormat.Format32bppArgb)) {
        var od = o.LockBits(new Rectangle(0,0,w,h), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
        Marshal.Copy(outb, 0, od.Scan0, outb.Length); o.UnlockBits(od); o.Save(dst, ImageFormat.Png);
      }
    }
  }
}
public static class Botanical3 {
  static double[] Blur(double[] a, int w, int h) { var o = new double[w*h];
    for (int y=0;y<h;y++) for (int x=0;x<w;x++) { double s=0; int c=0; for(int j=-1;j<=1;j++) for(int k=-1;k<=1;k++){int yy=y+j,xx=x+k; if(yy<0||yy>=h||xx<0||xx>=w) continue; s+=a[yy*w+xx]; c++;} o[y*w+x]=s/c; } return o; }
  static double Smooth(double e0, double e1, double x) { double t = Math.Max(0, Math.Min(1, (x-e0)/(e1-e0))); return t*t*(3-2*t); }
  public static void Run(string src, string dst, int size) {
    double t0=0.045, gain=7.0, washA=0.75, paperMix=0.25, fade=0.10;
    using (var im0 = new Bitmap(src)) using (var im = new Bitmap(im0, new Size(size, size))) {
      int w=size,h=size; var d = im.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
      var buf = new byte[w*h*4]; Marshal.Copy(d.Scan0, buf, 0, buf.Length); im.UnlockBits(d);
      var L = new double[w*h]; var S = new double[w*h];
      for (int i=0;i<w*h;i++){ double bb=buf[i*4]/255.0,g=buf[i*4+1]/255.0,r=buf[i*4+2]/255.0; L[i]=0.299*r+0.587*g+0.114*bb; double mx=Math.Max(r,Math.Max(g,bb)), mn=Math.Min(r,Math.Min(g,bb)); S[i]= mx<=0?0:(mx-mn)/mx; }
      var B = Blur(Blur(L,w,h),w,h);
      double pr=0xf4/255.0,pg=0xee/255.0,pb=0xe5/255.0, lr=0x5a/255.0,lg=0x26/255.0,lb=0x30/255.0;
      var outb = new byte[w*h*4];
      for (int y=1;y<h-1;y++) for (int x=1;x<w-1;x++) {
        int i=y*w+x;
        double gx = -B[i-w-1]-2*B[i-1]-B[i+w-1]+B[i-w+1]+2*B[i+1]+B[i+w+1];
        double gy = -B[i-w-1]-2*B[i-w]-B[i-w+1]+B[i+w-1]+2*B[i+w]+B[i+w+1];
        double line = Math.Min(1, Math.Max(0, (Math.Sqrt(gx*gx+gy*gy) - t0) * gain));
        double ink = Math.Max(1 - Smooth(0.86, 0.97, B[i]), Smooth(0.10, 0.25, S[i]));
        double edge = Math.Min(Math.Min(x, w-1-x), Math.Min(y, h-1-y)) / (double)w;
        double ef = Smooth(0, fade, edge);
        double wa = washA * ink * ef, la = line * 0.92 * ef;
        double r=buf[i*4+2]/255.0,g=buf[i*4+1]/255.0,bb=buf[i*4]/255.0, l=L[i];
        r = l + (r-l)*0.55; g = l + (g-l)*0.55; bb = l + (bb-l)*0.55;
        r = r*(1-paperMix)+pr*paperMix; g = g*(1-paperMix)+pg*paperMix; bb = bb*(1-paperMix)+pb*paperMix;
        double a = la + wa*(1-la);
        double cr = a<=0?0:(lr*la + r*wa*(1-la))/a, cg = a<=0?0:(lg*la + g*wa*(1-la))/a, cb = a<=0?0:(lb*la + bb*wa*(1-la))/a;
        outb[i*4]=(byte)((cb*a+pb*(1-a))*255); outb[i*4+1]=(byte)((cg*a+pg*(1-a))*255); outb[i*4+2]=(byte)((cr*a+pr*(1-a))*255); outb[i*4+3]=255;
      }
      for (int q=0;q<w*h;q++) if (outb[q*4+3]==0) { outb[q*4]=(byte)(pb*255); outb[q*4+1]=(byte)(pg*255); outb[q*4+2]=(byte)(pr*255); outb[q*4+3]=255; }
      using (var o = new Bitmap(w,h,PixelFormat.Format32bppArgb)) { var od=o.LockBits(new Rectangle(0,0,w,h), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb); Marshal.Copy(outb,0,od.Scan0,outb.Length); o.UnlockBits(od); var enc = Array.Find(ImageCodecInfo.GetImageEncoders(), e => e.MimeType == "image/jpeg"); var ep = new EncoderParameters(1); ep.Param[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Quality, 86L); o.Save(dst, enc, ep); }
    }
  }
}
"@
}
$CacheFull = (Resolve-Path $Cache).Path
foreach ($id in $notes) { if (-not (Test-Path "$CacheFull\eng\$id.png")) { [Engrave3]::Run("$CacheFull\notes\$id.jpg", "$CacheFull\eng\$id.png", 220, 99, 44, 53, 2.1, 0.45) } }
foreach ($id in $bots)  { if (-not (Test-Path "$CacheFull\bot\$id.jpg")) { [Botanical3]::Run("$CacheFull\notes\$id.jpg", "$CacheFull\bot\$id.jpg", 460) } }

$b64 = { param($p) [Convert]::ToBase64String([IO.File]::ReadAllBytes($p)) }
$c = [regex]::Replace($c, '\{\{IMG_(\d+)\}\}',  { param($m) 'data:image/jpeg;base64,' + (& $b64 "$CacheFull\$($m.Groups[1].Value).jpg") })
$c = [regex]::Replace($c, '\{\{NOTE_(\d+)\}\}', { param($m) 'data:image/png;base64,'  + (& $b64 "$CacheFull\eng\$($m.Groups[1].Value).png") })
$c = [regex]::Replace($c, '\{\{BOT_(\d+)\}\}',  { param($m) 'data:image/jpeg;base64,' + (& $b64 "$CacheFull\bot\$($m.Groups[1].Value).jpg") })
$left = [regex]::Matches($c, '\{\{[A-Z][A-Z0-9_]*\}\}') | ForEach-Object Value | Sort-Object -Unique
if ($left) { throw "Unfilled placeholders: $($left -join ', ')" }
$utf8 = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText($Out, $c, $utf8)
if ($Artifact) {
  # skeleton-free copy for the Artifact tool's main page: no doctype/head/body, no print button
  $a = [regex]::Replace($c, '(?is)<!doctype html>|<html[^>]*>|</?head>|</body>|</html>|<meta charset="utf-8">|<meta name="viewport"[^>]*>', '')
  $a = [regex]::Replace($a, '<body data-mode="(\w+)">', '<script>document.body.dataset.mode = "$1";</script>')
  $a = $a.Replace('<button class="pdf" onclick="window.print()">Zapisz PDF</button>', '')
  $a = $a.Replace('.switch-wrap { position:sticky; top:0;', '.switch-wrap { position:sticky; top:env(safe-area-inset-top, 0px);').TrimStart()
  [IO.File]::WriteAllText($Artifact, $a, $utf8)
}
"built $Out ($([math]::Round($c.Length/1KB)) KB)"
