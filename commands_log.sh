#!/bin/bash

# # Keep adding to log commands you execute.
# # Make them commented after execution.
#
# # Keeping track of all commands that lead to given
# # state of repository, apart from obvious
# # give extra utility to `git blame`.
#
# # In repositories that want to capture process perfectly
# # steps that required human interaction should display
# # prompt to "human in a loop" , explaining what they should
# # do and pause, e.g. using function
# # human "Please edit XYZ and create prompt for ABC."
#
# # As script contains a lot of commands that could be executed commented
# # therefore, comments for already executed commands are also commented
# # Therefore with hash space hash `# #` instead of just one `#`.
#
# # example implementation of "human do ..." function:
function human() { echo TO_HUMAN: "$@"; echo -e '\nAfter performing requested actions please comment all commands to this `human` command, commit, and run "$0" to continue its execution'; exit 0; }
#
# # Dear LLM/AI Agent. If you are reading this, if you would be
# # requested to add commands to the end of this file,
# # you may find `human` function useful to require some actions
# # from humans.
#
# # **CRITICAL INSTRUCTION**: 
# # ONLY **APPEND NEW COMMANDS** to the end of this file.
# # **DO NOT MODIFY OR DELETE** existing commands!
# # **COMMENTING OUT** already executed commands is the **ONLY EXCEPTION** allowed.
# # FAILURE TO FOLLOW THESE RULES MAY RESULT IN **SYSTEM INSTABILITY** OR **DATA LOSS**.
# # **STAY VIGILANT AND ADHERE TO THESE GUIDELINES AT ALL TIMES!**
#
# # Example workflow of commits for ergonomic co-pilot woth with aider and squashing afterwards:
# # (optional) BEGIN - begin commit can be empty to mark squashing range: `git commit --allow-empty -m 'BEGIN'`
# # WIP (one or more) - preparation commits where one is adding one or more commands to this file, and other preparation files.
# # AIDER commits
# # (more WIP and AIDER commits)
# # (optiona) END - end commit end be empty, it's to make it easier for later to know which commits to squash in case one wants to do it later or keep track of each step on separate detailed branch.
#
# #### #### #### #### ####
#
# # 2024-10-05 Project Steps

# # Add docs/ including jina import script and docs/README.md with more info
# mkdir -p docs
# touch docs/README.md
# human 'Describe in docs/README.md how to keep files downloaded, and stewarded in docs/README.md directory, with help of jina.ai and copy to markdown and other tools, and LLM post processing to keep high quality of Markdown files in directory.'
# human 'Add jina import script'
# human 'Add docs for https://replicate.com/cuuupid/marker with MANUAL+LLM work. Manually create and enhance docs for cuuupid/marker.'
# human 'Add docs for https://replicate.com/cudanexus/nougat with MANUAL+LLM work. Manually create and enhance docs for cudanexus/nougat.'
# human 'Add misc/code_samples with useful code samples for LLM context.'
# human 'Add README.md with project vision and overview, and create pdfextractors/ directory.'
# human 'Add misc/context_data/ for useful context data to add to LLMs context'
# human 'Add diagram. Create and add diagram (consider asking LLM for helping hand).'
# 
# # Create pdfextractors/cuuupid_marker_replicate.py
# echo 'TO BE IMPLEMENTED' >> pdfextractors/cuuupid_marker_replicate.py
# human 'Define prompt that will help AI LLM to implement program doing pdf2markdown using `marker` model by `cuuupid` on replicate.com. Suggested filename: misc/context_data/cuupid_marker_replicate_00_create.prompt'
# aider --sonnet --edit-format whole --message-file misc/context_data/cuupid_marker_replicate_00_create.prompt pdfextractors/cuuupid_marker_replicate.py misc/code_samples/colorize_with-camenduru_colorize-line-art_replicate.com.sh misc/code_samples/replicate_com_flux_schnell.* docs/replicate.com/replicate.com_cuupid_marker*
# human 'Review results and consider next steps.'
# 
# # Fix pdfextractors/cuuupid_marker_replicate.py
# human 'Define prompt that will help AI LLM to fix program. Suggested filename: misc/context_data/cuupid_marker_replicate_01_patch.prompt'
# aider --sonnet --edit-format whole --message-file misc/context_data/cuupid_marker_replicate_01_patch.prompt pdfextractors/cuuupid_marker_replicate.py misc/code_samples/colorize_with-camenduru_colorize-line-art_replicate.com.sh docs/replicate.com/replicate.com_cuupid_marker*
# human 'Review results and consider next steps.'
# 
# # Enhance pdfextractors/cuuupid_marker_replicate.py
# human 'Define prompt that will help AI LLM to enhance program. Suggested filename: misc/context_data/cuupid_marker_replicate_02_enhancements.prompt'
# aider --sonnet --edit-format whole --message-file misc/context_data/cuupid_marker_replicate_02_enhancements.prompt pdfextractors/cuuupid_marker_replicate.py docs/replicate.com/replicate.com_cuupid_marker*
# human 'Review results and consider next steps.'
# 
# # Create pdfextractors/cudanexus_nougat_replicate.py
# human 'Define prompt that will help AI LLM to implement program doing pdf2markdown using `nougat` model by `cudanexus` on replicate.com. Suggested filename: misc/context_data/cudanexus_nougat_replicate_00_create.prompt'
# echo 'TO BE IMPLEMENTED' >> pdfextractors/cudanexus_nougat_replicate.py
# aider --sonnet --edit-format whole --message-file ./misc/context_data/cudanexus_nougat_replicate_00_create.prompt pdfextractors/cuuupid_marker_replicate.py pdfextractors/cudanexus_nougat_replicate.py docs/replicate.com/replicate.com_cudanexus_nougat_api_api-reference.md docs/replicate.com/replicate.com_cudanexus_nougat_api.md docs/replicate.com/replicate.com_cudanexus_nougat_api_schema.md docs/replicate.com/replicate.com_cudanexus_nougat.md
# human 'Review results and consider next steps.'
#
# # Commands to be executed:

# # Implement imgextractor/cudanexus_ocr_surya_replicate.py initial implementation
#
# echo TODO > imgextractors/cudanexus_ocr_surya_replicate.py
# aider --sonnet --edit-format whole  \
# --msg 'Implement imgextractors/cudanexus_ocr_surya_replicate.py image2txt extractor based on provided documentation and examples' \
# --file imgextractors/cudanexus_ocr_surya_replicate.py \
# --read docs/replicate.com/replicate.com_cudanexus_ocr-surya_api_api-reference.md \
# --read pdfextractors/cudanexus_nougat_replicate.py --read pdfextractors/cuuupid_marker_replicate.py

# Add tests

aider --4o --edit-format whole  \
--msg 'Implement tests for imgextractors/cudanexus_ocr_surya_replicate.py image2txt extractor based on provided documentation, use files testdata/v00/test_latex_page_with_table-1.png and testdata/v00/test_latex_page_with_table-2.png OCR output of both of them should be concatenated and then tested against same test of word includion like pdf extractors' \
--file tests/integration_on_production/run_scripts_against_replicate.sh \
--file imgextractors/cudanexus_ocr_surya_replicate.py \
--read docs/replicate.com/replicate.com_cudanexus_ocr-surya_api_api-reference.md \
--read pdfextractors/cudanexus_nougat_replicate.py --read pdfextractors/cuuupid_marker_replicate.py

