#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python"]
inputs:
    script_plot:
        type: File?
        inputBinding:
            position: 1
    input_data:
        type: File?
        inputBinding:
            position: 2
    output_plot_name:
        type: string
        inputBinding:
            position: 3
outputs:
  img_out:
    type: File
    outputBinding:
      glob: '*.png'