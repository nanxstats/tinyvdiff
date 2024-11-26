# tinyvdiff

## Why tinyvdiff?

Designing a visual regression testing framework involves balancing several
competing challenges, particularly when it comes to the snapshot file format
used for comparisons. The ideal format must meet three seemingly conflicting
criteria:

1. **Support for diverse input types:** Graphics and documents are often
   generated using different tools and formats (e.g., PNG vs. PDF),
   making direct comparisons difficult.
2. **Bitwise reproducibility in plain text:** The format should capture the
   precise appearance of the output while being deterministic and easy to
   inspect visually.
3. **Platform independence:** Subtle differences in system fonts or
   dependencies can lead to inconsistent outputs across environments,
   yet the format should produce visually identical results on any system.

tinyvdiff takes a pragmatic approach by relaxing the third criterion and
making reasonable assumptions about the first to deliver a simple yet
effective solution:

1. Snapshots must be in **vector PDF** format, leaving it to developers to
   choose the tools and workflows for generating them.
2. PDFs are converted to **vector SVG** using `pdf2svg` for comparison.
3. We assume it is sufficient to run visual regression tests in a single
   CI/CD operating system environment. Snapshots should be generated in a
   similar OS environment to ensure consistency with the CI/CD system.

This approach keeps tinyvdiff lightweight and focused, making it a practical
choice for many visual regression testing workflows.
