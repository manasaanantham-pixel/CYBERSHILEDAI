import os
import math
import pefile
import joblib


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURES_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "malware_features.pkl"
)


def _safe_entropy(data):
    """
    Calculate entropy safely.
    """
    if not data:
        return 0.0

    try:
        pe_entropy = 0.0
        length = len(data)

        counts = [0] * 256

        for byte in data:
            counts[byte] += 1

        for count in counts:
            if count:
                probability = count / length
                pe_entropy -= probability * math.log2(probability)

        return pe_entropy

    except Exception:
        return 0.0


def extract_pe_features(file_path):
    """
    Extract the PE features required by the trained
    CyberShield AI malware model.
    """

    pe = pefile.PE(file_path)

    features = {}

    # =====================================================
    # DOS HEADER
    # =====================================================

    features["e_magic"] = pe.DOS_HEADER.e_magic
    features["e_cblp"] = pe.DOS_HEADER.e_cblp
    features["e_cp"] = pe.DOS_HEADER.e_cp
    features["e_crlc"] = pe.DOS_HEADER.e_crlc
    features["e_cparhdr"] = pe.DOS_HEADER.e_cparhdr
    features["e_minalloc"] = pe.DOS_HEADER.e_minalloc
    features["e_maxalloc"] = pe.DOS_HEADER.e_maxalloc
    features["e_ss"] = pe.DOS_HEADER.e_ss
    features["e_sp"] = pe.DOS_HEADER.e_sp
    features["e_csum"] = pe.DOS_HEADER.e_csum
    features["e_ip"] = pe.DOS_HEADER.e_ip
    features["e_cs"] = pe.DOS_HEADER.e_cs
    features["e_lfarlc"] = pe.DOS_HEADER.e_lfarlc
    features["e_ovno"] = pe.DOS_HEADER.e_ovno
    features["e_oemid"] = pe.DOS_HEADER.e_oemid
    features["e_oeminfo"] = pe.DOS_HEADER.e_oeminfo
    features["e_lfanew"] = pe.DOS_HEADER.e_lfanew

    # =====================================================
    # FILE HEADER
    # =====================================================

    file_header = pe.FILE_HEADER

    features["Machine"] = file_header.Machine
    features["NumberOfSections"] = file_header.NumberOfSections
    features["TimeDateStamp"] = file_header.TimeDateStamp
    features["PointerToSymbolTable"] = file_header.PointerToSymbolTable
    features["NumberOfSymbols"] = file_header.NumberOfSymbols
    features["SizeOfOptionalHeader"] = file_header.SizeOfOptionalHeader
    features["Characteristics"] = file_header.Characteristics

    # =====================================================
    # OPTIONAL HEADER
    # =====================================================

    optional = pe.OPTIONAL_HEADER

    features["Magic"] = optional.Magic
    features["MajorLinkerVersion"] = optional.MajorLinkerVersion
    features["MinorLinkerVersion"] = optional.MinorLinkerVersion
    features["SizeOfCode"] = optional.SizeOfCode
    features["SizeOfInitializedData"] = optional.SizeOfInitializedData
    features["SizeOfUninitializedData"] = optional.SizeOfUninitializedData
    features["AddressOfEntryPoint"] = optional.AddressOfEntryPoint
    features["BaseOfCode"] = optional.BaseOfCode
    features["ImageBase"] = optional.ImageBase
    features["SectionAlignment"] = optional.SectionAlignment
    features["FileAlignment"] = optional.FileAlignment
    features["MajorOperatingSystemVersion"] = optional.MajorOperatingSystemVersion
    features["MinorOperatingSystemVersion"] = optional.MinorOperatingSystemVersion
    features["MajorImageVersion"] = optional.MajorImageVersion
    features["MinorImageVersion"] = optional.MinorImageVersion
    features["MajorSubsystemVersion"] = optional.MajorSubsystemVersion
    features["MinorSubsystemVersion"] = optional.MinorSubsystemVersion
    features["SizeOfHeaders"] = optional.SizeOfHeaders
    features["CheckSum"] = optional.CheckSum
    features["SizeOfImage"] = optional.SizeOfImage
    features["Subsystem"] = optional.Subsystem
    features["DllCharacteristics"] = optional.DllCharacteristics
    features["SizeOfStackReserve"] = optional.SizeOfStackReserve
    features["SizeOfStackCommit"] = optional.SizeOfStackCommit
    features["SizeOfHeapReserve"] = optional.SizeOfHeapReserve
    features["SizeOfHeapCommit"] = optional.SizeOfHeapCommit
    features["LoaderFlags"] = optional.LoaderFlags
    features["NumberOfRvaAndSizes"] = optional.NumberOfRvaAndSizes

    # =====================================================
    # SECTION FEATURES
    # =====================================================

    sections = pe.sections

    features["SuspiciousImportFunctions"] = 0
    features["SuspiciousNameSection"] = 0
    features["SectionsLength"] = len(sections)

    section_entropies = []
    raw_sizes = []
    virtual_sizes = []
    physical_addresses = []
    virtual_addresses = []
    pointer_data = []
    characteristics = []

    for section in sections:

        try:
            entropy = section.get_entropy()
        except Exception:
            entropy = 0.0

        section_entropies.append(entropy)

        raw_sizes.append(section.SizeOfRawData)
        virtual_sizes.append(section.Misc_VirtualSize)

        physical_addresses.append(section.PointerToRawData)
        virtual_addresses.append(section.VirtualAddress)

        pointer_data.append(section.PointerToRawData)
        characteristics.append(section.Characteristics)

        # Suspicious section name check
        try:
            section_name = section.Name.decode(
                errors="ignore"
            ).strip("\x00").lower()

            suspicious_names = [
                "upx",
                "packed",
                "aspack",
                "petite",
                "themida",
                "vmprotect"
            ]

            if any(
                name in section_name
                for name in suspicious_names
            ):
                features["SuspiciousNameSection"] += 1

        except Exception:
            pass

    # =====================================================
    # SECTION STATISTICS
    # =====================================================

    if section_entropies:
        features["SectionMinEntropy"] = min(section_entropies)
        features["SectionMaxEntropy"] = max(section_entropies)
    else:
        features["SectionMinEntropy"] = 0
        features["SectionMaxEntropy"] = 0

    if raw_sizes:
        features["SectionMinRawsize"] = min(raw_sizes)
        features["SectionMaxRawsize"] = max(raw_sizes)
    else:
        features["SectionMinRawsize"] = 0
        features["SectionMaxRawsize"] = 0

    if virtual_sizes:
        features["SectionMinVirtualsize"] = min(virtual_sizes)
        features["SectionMaxVirtualsize"] = max(virtual_sizes)
    else:
        features["SectionMinVirtualsize"] = 0
        features["SectionMaxVirtualsize"] = 0

    if physical_addresses:
        features["SectionMaxPhysical"] = max(
            physical_addresses
        )
        features["SectionMinPhysical"] = min(
            physical_addresses
        )
    else:
        features["SectionMaxPhysical"] = 0
        features["SectionMinPhysical"] = 0

    if virtual_addresses:
        features["SectionMaxVirtual"] = max(
            virtual_addresses
        )
        features["SectionMinVirtual"] = min(
            virtual_addresses
        )
    else:
        features["SectionMaxVirtual"] = 0
        features["SectionMinVirtual"] = 0

    if pointer_data:
        features["SectionMaxPointerData"] = max(
            pointer_data
        )
        features["SectionMinPointerData"] = min(
            pointer_data
        )
    else:
        features["SectionMaxPointerData"] = 0
        features["SectionMinPointerData"] = 0

    if characteristics:
        features["SectionMaxChar"] = max(
            characteristics
        )
        features["SectionMainChar"] = characteristics[0]
    else:
        features["SectionMaxChar"] = 0
        features["SectionMainChar"] = 0

    # =====================================================
    # IMPORT / EXPORT / DIRECTORY FEATURES
    # =====================================================

    import_count = 0

    try:

        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):

            for entry in pe.DIRECTORY_ENTRY_IMPORT:

                for imported_function in entry.imports:

                    import_count += 1

                    if imported_function.name:

                        name = (
                            imported_function.name
                            .decode(
                                errors="ignore"
                            )
                            .lower()
                        )

                        suspicious = [
                            "virtualalloc",
                            "virtualprotect",
                            "writeprocessmemory",
                            "createremotethread",
                            "winexec",
                            "shellexecute",
                            "urldownloadtofile",
                            "internetopen",
                            "internetreadfile",
                            "loadlibrary",
                            "getprocaddress"
                        ]

                        if any(
                            x in name
                            for x in suspicious
                        ):
                            features[
                                "SuspiciousImportFunctions"
                            ] += 1

    except Exception:
        pass

    features["DirectoryEntryImport"] = import_count

    # Import directory
    try:

        import_directory = (
            pe.OPTIONAL_HEADER
            .DATA_DIRECTORY[
                pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]
            ]
        )

        features[
            "DirectoryEntryImportSize"
        ] = import_directory.Size

    except Exception:
        features["DirectoryEntryImportSize"] = 0

    # Export directory
    try:

        export_directory = (
            pe.OPTIONAL_HEADER
            .DATA_DIRECTORY[
                pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]
            ]
        )

        features[
            "DirectoryEntryExport"
        ] = export_directory.Size

        features[
            "ImageDirectoryEntryExport"
        ] = export_directory.VirtualAddress

    except Exception:

        features["DirectoryEntryExport"] = 0
        features["ImageDirectoryEntryExport"] = 0

    # Image directory entries
    directory_map = {
        "ImageDirectoryEntryImport":
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],

        "ImageDirectoryEntryResource":
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"],

        "ImageDirectoryEntryException":
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"],

        "ImageDirectoryEntrySecurity":
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
    }

    for feature_name, directory_id in directory_map.items():

        try:

            directory = (
                pe.OPTIONAL_HEADER
                .DATA_DIRECTORY[directory_id]
            )

            features[feature_name] = directory.VirtualAddress

        except Exception:

            features[feature_name] = 0

    # =====================================================
    # LOAD MODEL FEATURE ORDER
    # =====================================================

    feature_names = joblib.load(
        FEATURES_PATH
    )

    # Make sure every expected feature exists
    for feature in feature_names:

        if feature not in features:
            features[feature] = 0

    # Return only the features used during training
    ordered_features = {
        feature: features[feature]
        for feature in feature_names
    }

    return ordered_features
