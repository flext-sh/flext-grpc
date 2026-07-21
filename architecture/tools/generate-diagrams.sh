#!/bin/bash
# FLEXT-gRPC Architecture Diagram Generation Script
# Generates PNG, SVG, and ASCII diagrams from PlantUML sources

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
DIAGRAMS_DIR="${PROJECT_ROOT}/docs/architecture/diagrams"
OUTPUT_DIR="${PROJECT_ROOT}/docs/architecture/diagrams/generated"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
	echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
	echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
	echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
	echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
	log_info "Checking dependencies..."

	# Check for PlantUML
	if ! command -v plantuml &>/dev/null; then
		log_error "PlantUML not found. Please install PlantUML:"
		log_error "  - Ubuntu/Debian: sudo apt-get install plantuml"
		log_error "  - macOS: brew install plantuml"
		log_error "  - Manual: Download from https://plantuml.com/download"
		exit 1
	fi

	# Check for Java (required by PlantUML)
	if ! command -v java &>/dev/null; then
		log_error "Java not found. PlantUML requires Java to run."
		exit 1
	fi

	log_success "All dependencies found"
}

# Create output directories
setup_directories() {
	log_info "Setting up output directories..."

	mkdir -p "${OUTPUT_DIR}/png"
	mkdir -p "${OUTPUT_DIR}/svg"
	mkdir -p "${OUTPUT_DIR}/ascii"

	log_success "Output directories created"
}

# Generate diagrams from PlantUML files
generate_diagrams() {
	local format="$1"
	local output_subdir="$2"
	local plantuml_option="$3"

	log_info "Generating ${format} diagrams..."

	local count=0
	local success_count=0

	for puml_file in "${DIAGRAMS_DIR}"/*.puml; do
		if [[ -f $puml_file ]]; then
			local base_name=$(basename "$puml_file" .puml)
			local output_file="${OUTPUT_DIR}/${output_subdir}/${base_name}.${format}"

			log_info "  Processing: ${base_name}.puml → ${base_name}.${format}"

			if plantuml "${plantuml_option}" -o "${OUTPUT_DIR}/${output_subdir}" "$puml_file" 2>/dev/null; then
				log_success "    ✓ Generated: ${base_name}.${format}"
				((success_count++))
			else
				log_error "    ✗ Failed: ${base_name}.${format}"
			fi

			((count++))
		fi
	done

	log_info "Generated ${success_count}/${count} ${format} diagrams"
}

# Generate ASCII art versions using custom renderer
generate_ascii_diagrams() {
	log_info "Generating ASCII diagrams..."

	# This would require a PlantUML ASCII renderer
	# For now, we'll skip this as it's less commonly used
	log_warning "ASCII diagram generation not implemented yet"
	log_info "Consider using: plantuml -tutxt file.puml"
}

# Validate generated diagrams
validate_diagrams() {
	log_info "Validating generated diagrams..."

	local total_png=$(find "${OUTPUT_DIR}/png" -name "*.png" 2>/dev/null | wc -l)
	local total_svg=$(find "${OUTPUT_DIR}/svg" -name "*.svg" 2>/dev/null | wc -l)

	log_info "Found ${total_png} PNG files, ${total_svg} SVG files"

	# Check file sizes (basic validation)
	local empty_files=$(find "${OUTPUT_DIR}" -name "*.png" -o -name "*.svg" -size 0 2>/dev/null | wc -l)

	if [[ $empty_files -gt 0 ]]; then
		log_warning "Found ${empty_files} empty diagram files"
	else
		log_success "All diagram files have content"
	fi
}

# Generate index file for diagrams
generate_index() {
	log_info "Generating diagram index..."

	local index_file="${OUTPUT_DIR}/README.md"

	cat >"$index_file" <<'EOF'
# Generated Architecture Diagrams

This directory contains automatically generated architecture diagrams from PlantUML sources.

## Available Diagrams

EOF

	# Add PNG diagrams
	if [[ -d "${OUTPUT_DIR}/png" ]]; then
		echo "### PNG Diagrams" >>"$index_file"
		echo "" >>"$index_file"

		for png_file in "${OUTPUT_DIR}/png"/*.png; do
			if [[ -f $png_file ]]; then
				local base_name=$(basename "$png_file" .png)
				echo "- [${base_name}](${png_file}) - PNG format" >>"$index_file"
			fi
		done
		echo "" >>"$index_file"
	fi

	# Add SVG diagrams
	if [[ -d "${OUTPUT_DIR}/svg" ]]; then
		echo "### SVG Diagrams" >>"$index_file"
		echo "" >>"$index_file"

		for svg_file in "${OUTPUT_DIR}/svg"/*.svg; do
			if [[ -f $svg_file ]]; then
				local base_name=$(basename "$svg_file" .svg)
				echo "- [${base_name}](${svg_file}) - SVG format" >>"$index_file"
			fi
		done
		echo "" >>"$index_file"
	fi

	# Add generation info
	cat >>"$index_file" <<EOF

## Generation Information

- **Generated**: $(date)
- **Source**: PlantUML files in \`docs/architecture/diagrams/\`
- **Tool**: PlantUML $(plantuml -version 2>/dev/null | head -1 || echo "version unknown")
- **Script**: \`docs/architecture/tools/generate-diagrams.sh\`

## Usage

These diagrams follow the C4 Model for software architecture visualization:

- **Context Diagrams**: System scope and external interactions
- **Container Diagrams**: High-level technology choices
- **Component Diagrams**: Detailed component relationships
- **Deployment Diagrams**: Runtime infrastructure

## Maintenance

Diagrams are automatically regenerated when the PlantUML source files change. To manually regenerate all diagrams:

\`\`\`bash
cd docs/architecture/tools
./generate-diagrams.sh --all
\`\`\`
EOF

	log_success "Diagram index generated: ${index_file}"
}

# Main execution
main() {
	local generate_png=true
	local generate_svg=true
	local generate_ascii=false
	local skip_validation=false

	# Parse arguments
	while [[ $# -gt 0 ]]; do
		case $1 in
		--png-only)
			generate_svg=false
			generate_ascii=false
			shift
			;;
		--svg-only)
			generate_png=false
			generate_ascii=false
			shift
			;;
		--ascii)
			generate_ascii=true
			shift
			;;
		--skip-validation)
			skip_validation=true
			shift
			;;
		--help)
			echo "Usage: $0 [OPTIONS]"
			echo ""
			echo "Options:"
			echo "  --png-only       Generate only PNG diagrams"
			echo "  --svg-only       Generate only SVG diagrams"
			echo "  --ascii          Generate ASCII art diagrams"
			echo "  --skip-validation Skip diagram validation"
			echo "  --help           Show this help"
			exit 0
			;;
		*)
			log_error "Unknown option: $1"
			exit 1
			;;
		esac
	done

	log_info "Starting FLEXT-gRPC Architecture Diagram Generation"
	log_info "=================================================="

	check_dependencies
	setup_directories

	# Generate diagrams
	if [[ $generate_png == "true" ]]; then
		generate_diagrams "png" "png" ""
	fi

	if [[ $generate_svg == "true" ]]; then
		generate_diagrams "svg" "svg" "-tsvg"
	fi

	if [[ $generate_ascii == "true" ]]; then
		generate_ascii_diagrams
	fi

	# Validate and create index
	if [[ $skip_validation != "true" ]]; then
		validate_diagrams
	fi

	generate_index

	log_success "Architecture diagram generation completed!"
	log_info "Generated diagrams are available in: ${OUTPUT_DIR}"
}

# Run main function
main "$@"
