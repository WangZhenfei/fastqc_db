.headers on
select basic.filename, module_stats.overall from basic, module_stats where module_stats.overall = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_base_sequence_quality from basic, module_stats where module_stats.per_base_sequence_quality = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_tile_sequence_quality from basic, module_stats where module_stats.per_tile_sequence_quality = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_sequence_quality_scores from basic, module_stats where module_stats.per_sequence_quality_scores = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_base_sequence_content from basic, module_stats where module_stats.per_base_sequence_content = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_sequence_gc_content from basic, module_stats where module_stats.per_sequence_gc_content = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.per_base_n_content from basic, module_stats where module_stats.per_base_n_content = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.sequence_length_distribution from basic, module_stats where module_stats.sequence_length_distribution = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.sequence_duplication_levels from basic, module_stats where module_stats.sequence_duplication_levels = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.overrepresented_sequences from basic, module_stats where module_stats.overrepresented_sequences = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.adapter_content from basic, module_stats where module_stats.adapter_content = 'fail' AND module_stats.id = basic.id;
select basic.filename, module_stats.kmer_content from basic, module_stats where module_stats.kmer_content = 'fail' AND module_stats.id = basic.id;
