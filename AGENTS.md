# Hansi Ki Dhun workspace

Read README.md for the current library layout. New song projects belong in songs/<song_name>/, never at the workspace root. The maintained reusable starter is reusable_song_kit/starter/. Use tools/song_library.py new to scaffold if helpful.

Shared Whisper weights: shared/models/whisper-small/. Approved couple reference: shared/characters/approved_reference.png. Branding: shared/branding/. Kinetic typography reference and analysis: shared/kinetic_reference/.

Each song retains its own images, source audio, lyrics, timeline, renderer and final video. Preserve completed songs when creating new ones. Keep per-song render variations; do not replace them wholesale with the generic starter. Generate new images with imagegen and align each new audio independently. Existing word times are model estimates.

Refresh library.html/library.json/README.md with `python -X utf8 tools/song_library.py index` after a completed song is added. `python -X utf8 tools/song_library.py check` validates project paths, image readability, script syntax and video metadata.

The dated reorganization scripts are historical one-time migration tools, not normal cleanup commands. reports/reorganization_20261013/ records moved paths, original hashes, text backups and verified duplicate removal.
