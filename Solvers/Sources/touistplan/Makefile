###########################################################################
#                              OcamlMakefile
#                 Copyright (C) 1999, 2000, 2001  Markus Mottl
#
#                            For updates see:
#             http://miss.wu-wien.ac.at/~mottl/ocaml_sources
#
#        $Id: Makefile,v 1.2 2001/10/17 14:59:33 vince Exp $
#
###########################################################################


# Set these variables to the names of the sources to be processed and
# the result variable. Order matters during linkage!

OCAMLLEX = ocamllex

S = Sources/

SOURCES = \
	$(S)utils.ml \
	$(S)touist_solver.ml \
	$(S)smtsolver.ml \
	$(S)smtsolver_extractplan.ml \
	$(S)symb.ml \
	$(S)symbSet.ml \
	$(S)timedata.ml \
	$(S)functionFormula.ml \
	$(S)atom.ml \
	$(S)typeset.ml \
	$(S)formula.ml \
	$(S)constraintsType.ml \
	$(S)domain.ml \
	$(S)parser.mli\
	$(S)lexer.ml\
	$(S)parser.mly \
	$(S)node.ml \
	$(S)plan.ml \
	$(S)parallelPlan.ml \
	$(S)sequentialPlan.ml \
	$(S)planningData.ml \
	$(S)touistplan.ml \
	$(S)touistparse.ml \
	$(S)countConstraints.ml \
	$(S)tlpgp.ml \
	$(S)tsp.ml \
	$(S)tsp2.ml \
	$(S)main.ml

OCAMLFLAGS = -unsafe
# -pp "camlp4o ./p4.cmo"

LIBS = unix

RESULT = touistparse

ifndef SOURCES
  SOURCES := foo.ml
endif
export SOURCES

ifndef RESULT
  RESULT := foo
endif
export RESULT

export BCSUFFIX
export NCSUFFIX

ifndef TOPSUFFIX
  TOPSUFFIX := .top
endif

export TOPSUFFIX

# Eventually set include- and library-paths, libraries to link,
# additional compilation-, link- and ocamlyacc-flags
# Path- and library information needs not be written with "-I" and such...
# Define THREADS if you need it, otherwise leave it unset!

export THREADS
export UNIX

export INCDIRS
export LIBDIRS
export OCAML_DEFAULT_DIRS
export OCAML_LIB_INSTALL

export LIBS
export CLIBS

export OCAMLFLAGS
export OCAMLNCFLAGS
export OCAMLBCFLAGS

export OCAMLLDFLAGS
export OCAMLNLDFLAGS
export OCAMLBLDFLAGS

ifndef OCAMLCPFLAGS
  OCAMLCPFLAGS := a
endif

export OCAMLCPFLAGS

export YFLAGS
export IDLFLAGS

export CC
export CFLAGS
export LDFLAGS

# Add a list of optional trash files that should be deleted by "make clean"
export TRASH

####################  variables depending on your Ocaml-installation

BCRESULT  := $(addsuffix $(BCSUFFIX), $(RESULT))
NCRESULT  := $(addsuffix $(NCSUFFIX), $(RESULT))
TOPRESULT := $(addsuffix $(TOPSUFFIX), $(RESULT))

ifndef OCAMLC
  OCAMLC := ocamlc.opt
endif

export OCAMLC

ifndef OCAMLOPT
  OCAMLOPT := ocamlopt.opt
endif

export OCAMLOPT

ifndef OCAMLMKTOP
  OCAMLMKTOP := ocamlmktop
endif

export OCAMLMKTOP

ifndef OCAMLCP
  OCAMLCP := ocamlcp
endif

export OCAMLCP

ifndef OCAMLDEP
  OCAMLDEP := ocamldep
endif

export OCAMLDEP

ifndef OCAMLLEX
  OCAMLLEX := ocamllex.opt
endif

export OCAMLLEX

ifndef OCAMLYACC
  OCAMLYACC := ocamlyacc
endif

export OCAMLYACC

ifndef OCAMLIDL
  CAMLIDL := camlidl
endif

export OCAMLIDL

ifndef NOIDLHEADER
  MAYBE_IDL_HEADER := -header
endif

export NOIDLHEADER

ifndef OCAMLMAKEFILE
  OCAMLMAKEFILE := Makefile
endif

export OCAMLMAKEFILE

ifndef OCAMLLIBPATH
  OCAMLLIBPATH := \
    $(shell $(OCAMLC) 2>/dev/null -where || echo /usr/local/lib/ocaml)
endif

export OCAMLLIBPATH

ifndef OCAML_LIB_INSTALL
  OCAML_LIB_INSTALL := $(OCAMLLIBPATH)/contrib
endif

export OCAML_LIB_INSTALL


###########################################################################

####################  change following sections only if
####################    you know what you are doing!

# for pedants using "--warn-undefined-variables"
export MAYBE_IDL
export REAL_RESULT
export CAMLIDLFLAGS
export THREAD_FLAG

SHELL := /bin/sh

MLDEPDIR := ._d
BCDIDIR  := ._bcdi
NCDIDIR  := ._ncdi

FILTERED     := $(filter %.mli %.ml %.mll %.mly %.idl %.c, $(SOURCES))
SOURCE_DIRS  := $(filter-out ./, $(sort $(dir $(FILTERED))))

FILTERED_ML  := $(filter %.ml, $(FILTERED))
DEP_ML       := $(FILTERED_ML:%.ml=$(MLDEPDIR)/%.d)

FILTERED_MLI := $(filter %.mli, $(FILTERED))
DEP_MLI      := $(FILTERED_MLI:.mli=.di)

FILTERED_MLL := $(filter %.mll, $(FILTERED))
DEP_MLL      := $(FILTERED_MLL:%.mll=$(MLDEPDIR)/%.d)
AUTO_MLL     := $(FILTERED_MLL:.mll=.ml)

FILTERED_MLY := $(filter %.mly, $(FILTERED))
DEP_MLY      := $(FILTERED_MLY:%.mly=$(MLDEPDIR)/%.d) $(FILTERED_MLY:.mly=.di)
AUTO_MLY     := $(FILTERED_MLY:.mly=.mli) $(FILTERED_MLY:.mly=.ml)

FILTERED_IDL := $(filter %.idl, $(FILTERED))
DEP_IDL      := $(FILTERED_IDL:%.idl=$(MLDEPDIR)/%.d) $(FILTERED_IDL:.idl=.di)
C_IDL        := $(FILTERED_IDL:%.idl=%_idl.c) $(FILTERED_IDL:.idl=.h)
OBJ_C_IDL    := $(FILTERED_IDL:%.idl=%_idl.o)
AUTO_IDL     := $(FILTERED_IDL:.idl=.mli) $(FILTERED_IDL:.idl=.ml) $(C_IDL)

FILTERED_C   := $(filter %.c, $(FILTERED))
OBJ_C        := $(FILTERED_C:.c=.o)

AUTO_TARGETS := $(AUTO_MLL) $(AUTO_MLY) $(AUTO_IDL)

ALL_DEPS     := $(DEP_ML) $(DEP_MLI) $(DEP_MLL) $(DEP_MLY) $(DEP_IDL)
MLDEPS       := $(filter %.d, $(ALL_DEPS))
MLIDEPS      := $(filter %.di, $(ALL_DEPS))
BCDEPIS      := $(MLIDEPS:%.di=$(BCDIDIR)/%.di)
NCDEPIS      := $(MLIDEPS:%.di=$(NCDIDIR)/%.di)

ALLML        := $(filter %.mli %.ml %.mll %.mly %.idl, $(FILTERED))

IMPLO_INTF   := $(ALLML:%.mli=%.mli.__)
IMPLO_INTF   := $(foreach file, $(IMPLO_INTF), \
                  $(basename $(file)).cmi $(basename $(file)).cmo)
IMPLO_INTF   := $(filter-out %.mli.cmo, $(IMPLO_INTF))
IMPLO_INTF   := $(IMPLO_INTF:%.mli.cmi=%.cmi)

IMPLX_INTF   := $(IMPLO_INTF:.cmo=.cmx)

INTF         := $(filter %.cmi, $(IMPLO_INTF))
IMPL_CMO     := $(filter %.cmo, $(IMPLO_INTF))
IMPL_CMX     := $(IMPL_CMO:.cmo=.cmx)

OBJ_LINK     := $(OBJ_C_IDL) $(OBJ_C)
OBJ_FILES    := $(IMPL_CMO:.cmo=.o) $(OBJ_LINK)

EXECS        := $(sort $(TOPRESULT) $(BCRESULT) $(NCRESULT))

NONEXECS     := $(INTF) $(IMPL_CMO) $(IMPL_CMX) $(OBJ_FILES) $(AUTO_TARGETS) \
                $(BCRESULT).cma $(NCRESULT).cmxa $(NCRESULT).a

TARGETS      := $(EXECS) $(NONEXECS)

# If there are IDL-files
ifneq "$(strip $(FILTERED_IDL))" ""
  MAYBE_IDL := -cclib -lcamlidl
endif

INCFLAGS := $(SOURCE_DIRS:%=-I %) $(INCDIRS:%=-I %) $(OCAML_DEFAULT_DIRS:%=-I %)
CINCFLAGS := $(SOURCE_DIRS:%=-I%) $(INCDIRS:%=-I%) $(OCAML_DEFAULT_DIRS:%=-I%)

ifndef PROFILING
  INTF_OCAMLC := $(OCAMLC)
else
  ifndef THREADS
    INTF_OCAMLC := $(OCAMLCP) -p $(OCAMLCPFLAGS)
  else
    # OCaml does not support profiling byte code
    # with threads (yet), therefore we force an error.
    ifndef REAL_OCAMLC
      error
    endif
  endif
endif

COMMON_LDFLAGS := $(LDFLAGS:%=-ccopt %) $(SOURCE_DIRS:%=-ccopt -L%) \
                  $(LIBDIRS:%=-ccopt -L%) $(OCAML_DEFAULT_DIRS:%=-ccopt -L%)


OBJS_LIBS := $(OBJ_LINK) $(CLIBS:%=-cclib -l%) $(MAYBE_IDL)

# If we have to make byte-code
ifndef REAL_OCAMLC
  SPECIAL_OCAMLFLAGS := $(OCAMLBCFLAGS)

  REAL_OCAMLC := $(INTF_OCAMLC)

  REAL_IMPL := $(IMPL_CMO)
  REAL_IMPL_INTF := $(IMPLO_INTF)
  IMPL_SUF := .cmo

  DEPFLAGS  :=
  MAKE_DEPS := $(MLDEPS) $(BCDEPIS)

  ifndef THREADS
    ifneq "$(strip $(OBJ_LINK))" ""
      ALL_LDFLAGS := -custom
    endif
    ifdef CLIBS
      ALL_LDFLAGS := -custom
    endif
  endif

  ALL_LDFLAGS += $(INCFLAGS) $(OCAMLLDFLAGS) $(OCAMLBLDFLAGS) \
                 $(COMMON_LDFLAGS) $(LIBS:%=%.cma)

  ifdef THREADS
    ALL_LDFLAGS += -thread unix.cma threads.cma
    THREAD_FLAG := -thread
  endif

  ifdef UNIX
    ALL_LDFLAGS += unix.cma
  endif

# we have to make native-code
else
  ifndef PROFILING
    SPECIAL_OCAMLFLAGS := $(OCAMLNCFLAGS)
    PLDFLAGS :=
  else
    SPECIAL_OCAMLFLAGS := -p $(OCAMLNCFLAGS)
    PLDFLAGS := -p
  endif

  REAL_IMPL := $(IMPL_CMX)
  REAL_IMPL_INTF := $(IMPLX_INTF)
  IMPL_SUF := .cmx

  CFLAGS := -DNATIVE_CODE $(CFLAGS)

  DEPFLAGS  := -native
  MAKE_DEPS := $(MLDEPS) $(NCDEPIS)

  ALL_LDFLAGS := $(PLDFLAGS) $(INCFLAGS) $(OCAMLLDFLAGS) \
                 $(OCAMLNLDFLAGS) $(COMMON_LDFLAGS)

  ifndef CREATE_LIB
    ALL_LDFLAGS += $(LIBS:%=%.cmxa)
  endif

  ifdef THREADS
    ALL_LDFLAGS := -thread $(ALL_LDFLAGS)
    ifndef CREATE_LIB
      ALL_LDFLAGS += unix.cmxa threads.cmxa
    endif
    THREAD_FLAG := -thread
  endif

  ifdef UNIX
    ALL_LDFLAGS := unix.cmxa $(ALL_LDFLAGS)
  endif
endif

ALL_OCAMLCFLAGS := $(THREAD_FLAG) $(OCAMLFLAGS) \
                   $(INCFLAGS) $(SPECIAL_OCAMLFLAGS)

ifdef make_deps
  -include $(MAKE_DEPS)
  AUTO_TARGETS :=
endif

###########################################################################
# USER RULES

# generates byte-code (default)
byte-code:		$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT) \
				REAL_RESULT="$(BCRESULT)" make_deps=yes
bc:	byte-code

top:			$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(TOPRESULT) \
				REAL_RESULT="$(BCRESULT)" make_deps=yes

# generates native-code

native-code:		$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(NCRESULT) \
				REAL_RESULT="$(NCRESULT)" \
				REAL_OCAMLC="$(OCAMLOPT)" \
				make_deps=yes
nc:	native-code

# generates byte-code libraries
byte-code-library:	$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT).cma \
				REAL_RESULT="$(BCRESULT)" \
				CREATE_LIB=yes \
				make_deps=yes
bcl:	byte-code-library

# generates native-code libraries
native-code-library:	$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(NCRESULT).cmxa \
				REAL_RESULT="$(NCRESULT)" \
				REAL_OCAMLC="$(OCAMLOPT)" \
				CREATE_LIB=yes \
				make_deps=yes
ncl:	native-code-library

# generates byte-code with debugging information
debug-code:		$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT) \
				REAL_RESULT="$(BCRESULT)" make_deps=yes \
				OCAMLFLAGS="-g $(OCAMLFLAGS)" \
				OCAMLLDFLAGS="-g $(OCAMLLDFLAGS)"
dc:	debug-code

# generates byte-code libraries with debugging information
debug-code-library:	$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT).cma \
				REAL_RESULT="$(BCRESULT)" make_deps=yes \
				CREATE_LIB=yes \
				OCAMLFLAGS="-g $(OCAMLFLAGS)" \
				OCAMLLDFLAGS="-g $(OCAMLLDFLAGS)"
dcl:	debug-code-library

# generates byte-code for profiling
profiling-byte-code:		$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT) \
				REAL_RESULT="$(BCRESULT)" PROFILING="y" \
				make_deps=yes
pbc:	profiling-byte-code

# generates native-code

profiling-native-code:		$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(NCRESULT) \
				REAL_RESULT="$(NCRESULT)" \
				REAL_OCAMLC="$(OCAMLOPT)" \
				PROFILING="y" \
				make_deps=yes
pnc:	profiling-native-code

# generates byte-code libraries
profiling-byte-code-library:	$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(BCRESULT).cma \
				REAL_RESULT="$(BCRESULT)" PROFILING="y" \
				CREATE_LIB=yes \
				make_deps=yes
pbcl:	profiling-byte-code-library

# generates native-code libraries
profiling-native-code-library:	$(AUTO_TARGETS)
			@$(MAKE) -r -f $(OCAMLMAKEFILE) $(NCRESULT).cmxa \
				REAL_RESULT="$(NCRESULT)" PROFILING="y" \
				REAL_OCAMLC="$(OCAMLOPT)" \
				CREATE_LIB=yes \
				make_deps=yes
pncl:	profiling-native-code-library

###########################################################################
# LOW LEVEL RULES

$(REAL_RESULT):		$(REAL_IMPL_INTF) $(OBJ_LINK)
			$(REAL_OCAMLC) $(ALL_LDFLAGS) $(OBJS_LIBS) -o $@ \
				$(REAL_IMPL)

%$(TOPSUFFIX):		$(REAL_IMPL_INTF) $(OBJ_LINK)
			$(OCAMLMKTOP) $(ALL_LDFLAGS) $(OBJS_LIBS) -o $@ \
				$(REAL_IMPL)

.SUFFIXES:		.mli .ml .cmi .cmo .cmx .cma .cmxa .o \
                        .mly .di .d .a .idl .c .h

%.cma:			$(REAL_IMPL_INTF) $(OBJ_LINK)
			$(REAL_OCAMLC) -a $(ALL_LDFLAGS) $(OBJS_LIBS) -o $@ \
				$(OCAMLBLDFLAGS) $(REAL_IMPL)

%.cmxa %.a:		$(REAL_IMPL_INTF) $(OBJ_LINK)
			$(OCAMLOPT) -a $(ALL_LDFLAGS) $(OBJS_LIBS) \
				$(OCAMLNLDFLAGS) -o $@ $(REAL_IMPL)

.mli.cmi:
			$(INTF_OCAMLC) -c $(THREAD_FLAG) $(OCAMLFLAGS) \
				$(INCFLAGS) $<

.ml.cmi .ml.o .ml.cmx .ml.cmo:
			$(REAL_OCAMLC) -c $(ALL_OCAMLCFLAGS) $<

.PRECIOUS:		%.ml
%.ml:			%.mll
			$(OCAMLLEX) $<

.PRECIOUS:		%.ml %.mli
%.ml %.mli:		%.mly
			$(OCAMLYACC) $(YFLAGS) $<

.PRECIOUS:		%.ml %.mli %_idl.c %.h
%.ml %.mli %_idl.c %.h:		%.idl
			$(CAMLIDL) $(MAYBE_IDL_HEADER) $(IDLFLAGS) \
				$(CAMLIDLFLAGS) $<
			@if [ $(NOIDLHEADER) ]; then touch $*.h; fi;
			mv $*.c $*_idl.c

.c.o:
			$(CC) -c $(CFLAGS) $(CINCFLAGS) -I$(OCAMLLIBPATH) \
				$< -o $@

$(MLDEPDIR)/%.d:	%.ml
			@echo making $@ from $<
			@d=`dirname $@`; \
			  if [ ! -d $$d ]; then mkdir -p $$d; fi
			@$(OCAMLDEP) $(INCFLAGS) $< > $@

$(BCDIDIR)/%.di $(NCDIDIR)/%.di:	%.mli
			@echo making $@ from $<
			@d=`dirname $@`; \
			  if [ ! -d $$d ]; then mkdir -p $$d; fi
			@$(OCAMLDEP) $(DEPFLAGS) $(INCFLAGS) $< > $@

###########################################################################
# (UN)INSTALL RULES FOR LIBRARIES

.PHONY: libinstall
libinstall:	all
	@printf "\nInstalling library to: $(OCAML_LIB_INSTALL)\n"
	@printf "Is this ok? (y/[n]) - "
	@\
	  read ans; \
	  if [ "$$ans" != "y" ]; then \
	  	echo Installation aborted.; exit 1; fi
	@echo
	-install -d $(OCAML_LIB_INSTALL)
	for i in $(LIBINSTALL_FILES); \
	  do install -m 0644 $$i $(OCAML_LIB_INSTALL); done
	@printf "\nInstallation successful.\n"

.PHONY: libuninstall
libuninstall:
	@printf "\nUninstalling library from: $(OCAML_LIB_INSTALL)\n"
	@printf "Is this ok? (y/[n]) - "
	@\
	  read ans; \
	  if [ "$$ans" != "y" ]; then \
	  	echo Uninstallation aborted.; exit 1; fi
	@echo
	cd $(OCAML_LIB_INSTALL); rm $(LIBINSTALL_FILES)
	@printf "\nUninstallation successful.\n"

###########################################################################
# MAINTAINANCE RULES

.PHONY:	clean
clean:
	rm -f $(TARGETS) $(TRASH)
	rm -rf $(BCDIDIR) $(NCDIDIR) $(MLDEPDIR)

.PHONY:	cleanup
cleanup:
	rm -f $(NONEXECS) $(TRASH)
	rm -rf $(BCDIDIR) $(NCDIDIR) $(MLDEPDIR)

.PHONY: nobackup
nobackup:
	rm -f *.bak *~ *.dup
