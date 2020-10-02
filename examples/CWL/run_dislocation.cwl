#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python"]

inputs:
    script_run:
        type: File?
        inputBinding:
            position: 1

    output_run_name:
        type: string
        inputBinding:
            position: 2
outputs:
  dislocation_out:
    type: File
    outputBinding:
      glob: '*.json'