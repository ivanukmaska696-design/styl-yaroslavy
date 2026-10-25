import Foundation
import Vision
import CoreImage
import AppKit
// usage: cutout in.jpg out.png  -> person cut out on transparent background (macOS Vision, no downloads)
let inURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outURL = URL(fileURLWithPath: CommandLine.arguments[2])
guard let ci = CIImage(contentsOf: inURL, options: [.applyOrientationProperty: true]) else { print("ERR read"); exit(1) }
let req = VNGeneratePersonSegmentationRequest()
req.qualityLevel = .accurate
req.outputPixelFormat = kCVPixelFormatType_OneComponent8
let handler = VNImageRequestHandler(ciImage: ci, options: [:])
try handler.perform([req])
guard let mask = req.results?.first?.pixelBuffer else { print("ERR mask"); exit(1) }
var maskImg = CIImage(cvPixelBuffer: mask)
let sx = ci.extent.width / maskImg.extent.width, sy = ci.extent.height / maskImg.extent.height
maskImg = maskImg.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
let clear = CIImage(color: .clear).cropped(to: ci.extent)
let blend = CIFilter(name: "CIBlendWithMask")!
blend.setValue(ci, forKey: kCIInputImageKey)
blend.setValue(clear, forKey: kCIInputBackgroundImageKey)
blend.setValue(maskImg, forKey: kCIInputMaskImageKey)
let ctx = CIContext()
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
try ctx.writePNGRepresentation(of: blend.outputImage!, to: outURL, format: .RGBA8, colorSpace: cs)
print("ok", Int(ci.extent.width), Int(ci.extent.height))
