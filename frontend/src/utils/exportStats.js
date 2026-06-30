import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

const EXPORT_BG = "#0D1B2A";

async function captureElement(element) {
  if (!element) throw new Error("Nothing to export");
  return html2canvas(element, {
    backgroundColor: EXPORT_BG,
    scale: 2,
    useCORS: true,
    logging: false,
  });
}

export async function exportElementAsPng(element, filename = "mmrac1ng-stats.png") {
  const canvas = await captureElement(element);
  const link = document.createElement("a");
  link.download = filename;
  link.href = canvas.toDataURL("image/png");
  link.click();
}

export async function exportElementAsPdf(element, filename = "mmrac1ng-stats.pdf") {
  const canvas = await captureElement(element);
  const imgData = canvas.toDataURL("image/png");
  const w = canvas.width;
  const h = canvas.height;

  const pdf = new jsPDF({
    orientation: w > h ? "landscape" : "portrait",
    unit: "px",
    format: [w, h],
  });
  pdf.addImage(imgData, "PNG", 0, 0, w, h);
  pdf.save(filename);
}
