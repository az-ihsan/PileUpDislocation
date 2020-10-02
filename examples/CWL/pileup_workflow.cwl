#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    script_run: File
    script_plot: File
    output_run_name: string
    output_plot_name: string

outputs:
    run_simulation:
        type: File 
        outputSource: [run_dislocation/dislocation_out]

    plot_simulation:
        type: File
        outputSource: [plot/img_out]
steps:
    run_dislocation:
        run: run_dislocation.cwl
        in:
            script_run: script_run
            output_run_name: output_run_name
        out: [dislocation_out]

    plot:
        run: plot_dislocation.cwl
        in:
            script_plot: script_plot
            input_data: run_dislocation/dislocation_out
            output_plot_name: output_plot_name
        out: [img_out]
